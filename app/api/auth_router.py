from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import AuthServiceDep
from app.core.security import gerar_token
from app.schemas import UsuarioCreate, UsuarioLogin, UsuarioResponse

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@auth_router.post("/cadastrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(usuario_schema: UsuarioCreate, service: AuthServiceDep):
    usuario = await service.cadastrar_usuario(usuario_schema)
    return usuario

@auth_router.post("/login")
async def login(usuario_schema: UsuarioLogin, service: AuthServiceDep):
    usuario = await service.login(usuario_schema.email, usuario_schema.senha)
    
    access_token = gerar_token(usuario.id)
    refresh_token = gerar_token(usuario.id, timedelta(days=30))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login-form")
async def login_form(service: AuthServiceDep, formulario: OAuth2PasswordRequestForm = Depends()):
    usuario = await service.login(formulario.username, formulario.password)

    access_token = gerar_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
