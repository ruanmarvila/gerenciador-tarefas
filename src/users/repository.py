from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User:
        user = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return user.scalar_one()

    async def get_by_email(self, user_email: str) -> User | None:
        user = await self.session.execute(
            select(User).where(User.email == user_email)
        )
        return user.scalar_one_or_none()
    
    async def email_exists(self, user_email: str) -> bool:
        email = await self.session.execute(
            select(User.email).where(User.email == user_email)
        )
        return email.scalar_one_or_none() is not None

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        user.deleted_at = func.now()

    async def restore(self, user: User) -> User:
        user.deleted_at = None
        return user
    
    async def update_profile(self, user: User, data: dict) -> User:
        for field, value in data.items():
            if value is not None:
             setattr(user, field, value)
        
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return await self.get_by_id(user.id)


    async def update_password(self, user: User, new_password: str) -> None:
        user.password = new_password