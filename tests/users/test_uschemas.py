import pytest
from pydantic_core import ValidationError

from src.users.schemas import PasswordUpdate, UserCreate, UserLogin, UserUpdate


def test_create_user_schema():
    user = UserCreate(
        name="Ana",
        email="ana@gmail.com",
        password="12345678"
    )

    assert user.name is not None


@pytest.mark.parametrize("schema", [UserCreate, UserUpdate])
def test_schema_rejects_empty_name(schema):
    data = {
        "name": "",
        "email": "ana@gmail.com"
    }

    if schema is UserCreate:
        data["password"] = "12345678"

    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert "name" in str(exc_info.value)


@pytest.mark.parametrize("schema", [UserCreate, UserLogin])
def test_schema_rejects_invalid_email(schema):
    data = {
        "email": "invalid-email",
        "password": "12345678"
    }

    if schema is UserCreate:
        data["name"] = "Ana"

    with pytest.raises(ValidationError) as exc_info:
        schema(**data)
    
    assert "email" in str(exc_info.value)


@pytest.mark.parametrize("schema", [UserCreate, UserLogin])
def test_schema_rejects_short_password(schema):
    data = {
        "email": "ana@gmail.com",
        "password": "1234567"
    }

    if schema is UserCreate:
        data["name"] = "Ana"

    with pytest.raises(ValidationError) as exc_info:
        schema(**data)
        
    assert "password" in str(exc_info.value)


@pytest.mark.parametrize("name, email",[
    ("Ana", "ana@gmail.com"),
    (None, "ana@gmail.com"),
    ("Ana", None),
    (None, None)
    ],
)
def test_user_update_allows_none_values(name, email):
    user = UserUpdate(
        name= name,
        email= email
    )

    assert user.name == name
    assert user.email == email

def test_password_update_schema():
    update = PasswordUpdate(
        password= "12345678",
        new_password= "87654321"
    )

    assert update.new_password is not None

@pytest.mark.parametrize("password, new_password", [
    ("12345678", ""),
    ("", "12345678"),
    ("", "")
    ],
)
def test_password_update_requires_both_password_fields(password, new_password):
    with pytest.raises(ValidationError) as exc_info:
        PasswordUpdate(
            password= password,
            new_password= new_password
        )

    assert "password" in str(exc_info.value) or "new_password" in str(exc_info.value)


