from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('name', 'password')
    @classmethod
    def validate_not_empty(cls, value:str) -> str:
        if not value.strip():
            raise ValueError("The field cannot be empty")
        return value.strip()

class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("the field cannot be empty")
        return value.strip()


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None


class PasswordUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    @field_validator('password', 'new_password')
    @classmethod
    def validate_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("The field cannot be empty")
        return value.strip()


class UserPublic(BaseModel):
    name: str
    email: EmailStr


class UserPrivate(UserPublic):
    id: int