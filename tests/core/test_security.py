import jwt
import pytest

from src.core.config import settings
from src.core.exceptions import InvalidCredentialsError
from src.core.security import verify_refresh_token, verify_token


def test_verify_token_without_user_id(user):
    token = jwt.encode(
        {"email": user.email},
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    with pytest.raises(InvalidCredentialsError, match="Token without user_id"):
        verify_token(token)

def test_verify_token_with_invalid_token(user):
    token = jwt.encode(
        {"user_id": user.id},
        "fhke4B6M467lZerJxFTwUTyMmSkpAFdBiI40qirJ2fg",
        settings.ALGORITHM,
    )

    with pytest.raises(InvalidCredentialsError, match="Invalid access token"):
        verify_token(token)

def test_verify_refresh_token_without_user_id(user):
    token = jwt.encode(
        {"email": user.email},
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    with pytest.raises(InvalidCredentialsError, match="Token without user_id"):
        verify_refresh_token(token)

def test_verify_refresh_token_with_invalid_token(user):
    token = jwt.encode(
        {"user_id": user.id},
        "fhke4B6M467lZerJxFTwUTyMmSkpAFdBiI40qirJ2fg",
        settings.ALGORITHM,
    )

    with pytest.raises(InvalidCredentialsError, match="Invalid refresh token"):
        verify_refresh_token(token)