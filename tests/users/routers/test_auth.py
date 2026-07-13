import pytest
from fastapi import status
from freezegun import freeze_time


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/auth/create",
        json = {
            "name": "Ana",
            "email": "ana@gmail.com",
            "password": "12345678"
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["name"] == "Ana"
    assert data["email"] == "ana@gmail.com"

@pytest.mark.asyncio
async def test_create_user_with_short_password(client):
    response = await client.post(
        "/api/v1/auth/create",
        json = {
            "name": "Ana",
            "email": "ana@gmail.com",
            "password": "1234567"
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.asyncio
async def test_create_user_with_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/create",
        json = {
            "name": "Ana",
            "email": "invalid",
            "password": "12345678"
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.asyncio
async def test_create_user_with_existing_email(client, user):
    response = await client.post(
        "/api/v1/auth/create",
        json = {
            "name": "Ana",
            "email": user.email,
            "password": "12345678"
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "A user with this email already exists."

@pytest.mark.asyncio
async def test_login_returns_tokens(client, user):
    response = await client.post(
        "/api/v1/auth/token",
        data ={"username": user.email, "password": user.clean_password}
    )
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in token
    assert "refresh_token" in token
    assert "token_type" in token

@pytest.mark.asyncio
async def test_use_expired_access_token_returns_unauthorized(client, user):
    with freeze_time("2026-07-08 12:00:00"):
        response = await client.post(
        "/api/v1/auth/token",
        data = {"username": user.email, "password": user.clean_password},
    )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

    with freeze_time("2026-07-08 13:01:00"):
        response = await client.get(
            "/api/v1/users/me",
            headers = {"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Access token expired"

@pytest.mark.asyncio
async def test_login_with_nonexistent_email(client):
    response = await client.post(
        "/api/v1/auth/token",
        data = {"username": "invalid@invalid.com", "password": "12345678"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."

@pytest.mark.asyncio
async def test_login_with_wrong_password(client, user):
    response = await client.post(
        "/api/v1/auth/token",
        data = {"username": user.email, "password": "wrong_password"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."

@pytest.mark.asyncio
async def test_login_with_disable_account(client, user, token):
    response = await client.delete(
        "/api/v1/users/delete",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.post(
        "/api/v1/auth/token",
        data = {"username": user.email, "password": user.clean_password},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Account disabled. Please reactivate your account."

@pytest.mark.asyncio
async def test_refresh_token_returns_new_access_token(client, user, refresh_token):
    response = await client.post(
        "/api/v1/auth/refresh",
        headers = {"x-refresh-token": refresh_token},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

@pytest.mark.asyncio
async def test_refresh_with_expired_token_returns_unauthorized(client, user):
    with freeze_time("2026-07-08 12:00:00"):
        response = await client.post(
            "/api/v1/auth/token",
            data = {"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()["refresh_token"]
    
    with freeze_time("2026-08-08 12:01:00"):
        response = await client.post(
            "/api/v1/auth/refresh",
            headers = {"x-refresh-token": token},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Refresh token expired"

@pytest.mark.asyncio
async def test_restore_deleted_user_successfully(client, user, token):
    response = await client.delete(
        "/api/v1/users/delete",
        headers = {"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.post(
        "/api/v1/auth/restore",
        json = {
            "email": user.email,
            "password": user.clean_password
        },
    )

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == user.name
    assert data["email"] == user.email

@pytest.mark.asyncio
async def test_restore_user_with_invalid_credentials(client, user, token):
    response = await client.delete(
        "/api/v1/users/delete",
        headers = {"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.post(
        "/api/v1/auth/restore",
        json = {
            "email": "wrong@wrong.com",
            "password": user.clean_password
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."

@pytest.mark.asyncio
async def test_restore_already_active_user_returns_conflict(client, user):
    response = await client.post(
        "/api/v1/auth/restore",
        json = {
            "email": user.email,
            "password": user.clean_password
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Account is already activate."