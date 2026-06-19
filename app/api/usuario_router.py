from fastapi import APIRouter, status

from app.core.dependencies import UserServiceDep, UsuarioLogadoDep
from app.schemas import PerfilResponse, SenhaUpdate, UsuarioLogin, UsuarioResponse, UsuarioUpdate

usuario_router = APIRouter(
    prefix="/api/v1/usuarios", 
    tags=["usuários"]
)

@usuario_router.get("/", response_model=PerfilResponse)
async def perfil(usuario_logado: UsuarioLogadoDep, session:UserServiceDep):
    return await session.perfil(usuario_logado)

@usuario_router.patch("/editar", response_model=PerfilResponse)
async def editar(usuario_schema: UsuarioUpdate, usuario_logado: UsuarioLogadoDep, session: UserServiceDep):
    return await session.editar_perfil(usuario_schema, usuario_logado)

@usuario_router.patch("/editar/senha")
async def editar_senha(senha_schema: SenhaUpdate, usuario_logado: UsuarioLogadoDep, session: UserServiceDep):
    await session.editar_senha(senha_schema, usuario_logado)
    return {"mensagem": "senha alterada com sucesso"}

@usuario_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def excluir(usuario_logado: UsuarioLogadoDep, session: UserServiceDep):
    await session.deletar_conta(usuario_logado)

@usuario_router.post("/recuperar", response_model=UsuarioResponse)
async def recuperar(usuario_schema: UsuarioLogin, session: UserServiceDep):
    return await session.recuperar_conta(usuario_schema)
