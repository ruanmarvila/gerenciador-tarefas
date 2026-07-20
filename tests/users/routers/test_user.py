import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_user(client, user, token):
    response = await client.get(
        "/api/v1/users/me",
        headers = {"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == user.name
    assert data["email"] == user.email
    assert data["id"] == user.id

@pytest.mark.asyncio
async def test_get_user_without_token_returns_unauthorized(client):
    response = await client.get(
        "/api/v1/users/me"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid access token"

@pytest.mark.asyncio
async def test_refresh_token_cannot_access_get_user(client, refresh_token):
    response = await client.get(
        "api/v1/users/me",
        headers = {"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
@pytest.mark.parametrize("name, email",[
    ("Ana", "anaclara@gmail.com"),
    (None, "ruan@gmail.com"),
    ("Ruan", None),
    (None, None)
    ],
)
async def test_update_user(name, email, client, user, token):
    response = await client.patch(
        "/api/v1/users/update",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "name": name,
            "email": email
        },
    )

    expected_name = name or user.name
    expected_email = email or user.email
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == expected_name
    assert data["email"] == expected_email

@pytest.mark.asyncio
async def test_update_user_with_invalid_fields(client, token):
    response = await client.patch(
        "/api/v1/users/update",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "name": "",
            "email": ""
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.asyncio
async def test_update_password_successfully(client, user, token):
    response = await client.patch(
        "/api/v1/users/update/password",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "password": user.clean_password,
            "new_password": "balela2026"
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "password successfully updated"

@pytest.mark.asyncio
async def test_update_password_rejects_same_password(client, user, token):
    response = await client.patch(
        "/api/v1/users/update/password",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "password": user.clean_password,
            "new_password": user.clean_password
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "New password cannot be the same as the current password."

@pytest.mark.asyncio
async def test_update_password_with_wrong_current_password(client, token):
    response = await client.patch(
        "/api/v1/users/update/password",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "password": "wrong_password",
            "new_password": "balela2026"
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."

@pytest.mark.asyncio
async def test_delete_user(client, token):
    response = await client.delete(
        "/api/v1/users/delete",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio
async def test_delete_user_without_token_returns_unauthorized(client):
    response = await client.delete(
        "/api/v1/users/delete",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid access token"