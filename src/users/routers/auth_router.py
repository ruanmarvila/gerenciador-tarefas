from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import create_access_token, create_refresh_token
from src.users.dependencies import UserRefreshTokenDep, UserServiceDep
from src.users.schemas import UserCreate, UserLogin, UserPublic

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)


@router.post("/create", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user_schema: UserCreate, service: UserServiceDep):
    usuario = await service.create_user(user_schema)
    return usuario


@router.post("/token")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserServiceDep):
    user = await service.login(form.username, form.password)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@router.post("/refresh")
async def refresh(user: UserRefreshTokenDep):
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

@router.post("/restore", response_model=UserPublic)
async def restore(user_schema: UserLogin, service: UserServiceDep):
    return await service.restore_account(user_schema)