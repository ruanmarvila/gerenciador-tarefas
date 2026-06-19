from typing import Annotated

from fastapi import Depends
from sqlalchemy.future import select

from app.core.database import DBSession
from app.core.security import verificar_token
from app.exceptions import UsuarioNaoEncontradoError
from app.models import Usuario
from app.repositories import TarefaRepository, UsuarioRepository
from app.services import AuthService, TarefaService, UsuarioService


def get_user_repository(session: DBSession) -> UsuarioRepository:
    return UsuarioRepository(session)

UserRepositoryDep = Annotated[UsuarioRepository, Depends(get_user_repository)]


def get_auth_service(repo: UserRepositoryDep) -> AuthService:
    return AuthService(repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(repo: UserRepositoryDep) -> UsuarioService:
    return UsuarioService(repo)

UserServiceDep = Annotated[UsuarioService, Depends(get_user_service)]


def get_task_repository(session: DBSession) -> TarefaRepository:
    return TarefaRepository(session)

TaskRepositoryDep = Annotated[TarefaRepository, Depends(get_task_repository)]


def get_task_service(repo: TaskRepositoryDep) -> TarefaService:
    return TarefaService(repo)

TaskServiceDep = Annotated[TarefaService, Depends(get_task_service)]


async def obter_usuario_logado(session: DBSession, usuario_id: int = Depends(verificar_token)) -> Usuario:
    resultado = await session.execute(
        select(Usuario).where(Usuario.id == usuario_id)
    )
    usuario = resultado.scalar_one_or_none()

    if not usuario:
        raise UsuarioNaoEncontradoError()

    await session.commit()
    return usuario

UsuarioLogadoDep = Annotated[Usuario, Depends(obter_usuario_logado)]
