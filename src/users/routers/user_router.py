from fastapi import APIRouter, status

from src.users.dependencies import CurrentUserDep, UserServiceDep
from src.users.schemas import PasswordUpdate, UserPrivate, UserUpdate

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.get("/me", response_model=UserPrivate)
async def profile(current_user: CurrentUserDep, service:UserServiceDep):
    return await service.profile(current_user)

@router.patch("/update", response_model=UserPrivate)
async def update(user_schema: UserUpdate, current_user: CurrentUserDep, service: UserServiceDep):
    return await service.update_profile(user_schema, current_user)

@router.patch("/update/password")
async def update_password(senha_schema: PasswordUpdate, current_user: CurrentUserDep, service: UserServiceDep):
    await service.update_password(senha_schema, current_user)
    return {"message": "password successfully updated"}

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(current_user: CurrentUserDep, service: UserServiceDep):
    await service.delete_account(current_user)