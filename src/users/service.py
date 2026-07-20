from datetime import UTC, datetime, timedelta

from src.core.security import encrypt_password, verify_password
from src.users.exceptions import (
    AccountAlreadyActivateError,
    AccountDisabledError,
    AuthenticationError,
    EmailAlreadyExistsError,
    PasswordReuseError,
    UserNotFoundError,
)
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import PasswordUpdate, UserCreate, UserLogin, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def create_user(self, user_schema: UserCreate) -> User:
        if await self.repo.email_exists(user_schema.email):
            raise EmailAlreadyExistsError()
        
        hashed_password = encrypt_password(user_schema.password)
        new_user = User(name=user_schema.name,
                        email=user_schema.email,
                        password=hashed_password)
        
        user = await self.repo.add(new_user)
        await self.repo.session.commit()
        return user
    
    async def login(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password):
            raise AuthenticationError()
        
        if user.deleted_at:
            recovery_deadline = user.deleted_at + timedelta(days=30)
            if recovery_deadline > datetime.now(UTC):
                raise AccountDisabledError()
            
            raise UserNotFoundError()
        
        return user

    async def profile(self, current_user: User) -> User:
        user = await self.repo.get_by_id(current_user.id)
        return user
    
    async def update_profile(self, user_schema: UserUpdate, current_user: User) -> User:
        user = await self.repo.get_by_id(current_user.id)

        data = user_schema.model_dump()

        updated_user = await self.repo.update_profile(user, data)
        await self.repo.session.commit()
        return updated_user
    
    async def update_password(self, password_schema: PasswordUpdate, current_user: User) -> None:
        if password_schema.password == password_schema.new_password:
            raise PasswordReuseError()
        
        user = await self.repo.get_by_id(current_user.id)

        if not user or not verify_password(password_schema.password, user.password):
            raise AuthenticationError()
        
        new_hashed_password = encrypt_password(password_schema.new_password)
        await self.repo.update_password(user, new_hashed_password)
        await self.repo.session.commit()

    async def delete_account(self, current_user: User) -> None:
        user = await self.repo.get_by_id(current_user.id)
        await self.repo.delete(user)
        await self.repo.session.commit()

    async def restore_account(self, user_schema: UserLogin) -> User:
        user = await self.repo.get_by_email(user_schema.email)

        if not user or not verify_password(user_schema.password, user.password):
            raise AuthenticationError()
        
        if user.deleted_at is None:
            raise AccountAlreadyActivateError()
        
        recovery_deadline = user.deleted_at + timedelta(days=30)
        if recovery_deadline < datetime.now(UTC):
            raise UserNotFoundError()

        restored_user = await self.repo.restore(user)
        await self.repo.session.commit()
        return restored_user
