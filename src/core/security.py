#import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from src.core.config import settings
from src.core.exceptions import InvalidCredentialsError

pwd_hash = PasswordHash((Argon2Hasher(),))
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

def encrypt_password(password: str) -> str:
    return pwd_hash.hash(password)

def verify_password(normal_password: str, hashed_password: str) -> bool:
    return pwd_hash.verify(normal_password, hashed_password)

def generate_token(user_id: int, duration: timedelta = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    expiration_date = datetime.now(UTC) + duration
    info = {
        "user_id": user_id,
        "exp": expiration_date
    }
    return jwt.encode(info, settings.SECRET_KEY, settings.ALGORITHM)

def create_token(user_id: int, token_type: str, duration: timedelta = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    expiration_date = datetime.now(UTC) + duration
    info = {
        "user_id": user_id,
        "type": token_type,
        "exp": expiration_date
    }
    return jwt.encode(info, settings.SECRET_KEY, settings.ALGORITHM)

def create_access_token(user_id: int) -> str:
    return create_token(user_id, "access_token")

def create_refresh_token(user_id: int) -> str:
    return create_token(user_id, "refresh_token", timedelta(days=30))

def verify_token(token: str = Depends(oauth2_schema)) -> int:
    try:
        info = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = info.get("user_id")

        if user_id is None:
            raise InvalidCredentialsError("Token without user_id")
        
        return int(user_id)
    
    except ExpiredSignatureError as err:
        raise InvalidCredentialsError("Access token expired") from err
    except InvalidTokenError as err:
        raise InvalidCredentialsError("Invalid access token") from err
    except (TypeError, ValueError) as err:
        raise InvalidCredentialsError() from err

def verify_refresh_token(token: str) -> int:
    try:
        info = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = info.get("user_id")

        if user_id is None:
            raise InvalidCredentialsError("Token without user_id")
        
        return int(user_id)
    
    except ExpiredSignatureError as err:
        raise InvalidCredentialsError("Refresh token expired") from err
    except InvalidTokenError as err:
        raise InvalidCredentialsError("Invalid refresh token") from err
    except (TypeError, ValueError) as err:
        raise InvalidCredentialsError() from err