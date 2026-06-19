import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.exceptions import TokenInvalidoError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # type: ignore

pwd_hash = PasswordHash((Argon2Hasher(),))
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login-form", auto_error=False)

def criptografar_senha(senha: str) -> str:
    return pwd_hash.hash(senha)

def verificar_senha(normal_senha: str, hashed_senha: str) -> bool:
    return pwd_hash.verify(normal_senha, hashed_senha)

def gerar_token(usuario_id: int, duracao = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    data_expiracao = datetime.now(UTC) + duracao
    info = {
        "user_id": usuario_id,
        "exp": data_expiracao
    }
    return jwt.encode(info, SECRET_KEY, ALGORITHM)

def verificar_token(token: str = Depends(oauth2_schema)) -> int:
    try:
        info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        usuario_id = int(info.get("user_id")) # type: ignore
    except InvalidTokenError as err:
        raise TokenInvalidoError() from err
    
    return usuario_id

def verificar_refresh_token(token: str) -> int:
    try:
        info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        usuario_id = int(info.get("user_id")) # type: ignore
    except InvalidTokenError as err:
        raise TokenInvalidoError() from err
    
    return usuario_id