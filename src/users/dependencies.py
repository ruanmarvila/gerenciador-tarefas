from typing import Annotated

from fastapi import Depends
from sqlalchemy.future import select

from src.core.database import DBSession
from src.core.security import verify_access_token, verify_refresh_token
from src.users.exceptions import AccountDisabledError, UserNotFoundError
from src.users.models import User
from src.users.repository import UserRepository
from src.users.service import UserService


def get_user_repository(session: DBSession) -> UserRepository:
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(session: DBSession, user_id: int = Depends(verify_access_token)) -> User:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise UserNotFoundError()

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_user_via_refresh_token(session: DBSession, user_id: int = Depends(verify_refresh_token)) -> User:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise UserNotFoundError()
    
    if user.deleted_at:
        raise AccountDisabledError()
    
    return user

UserRefreshTokenDep = Annotated[User, Depends(get_user_via_refresh_token)]

