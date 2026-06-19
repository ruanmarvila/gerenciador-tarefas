from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Usuario


class UsuarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def buscar_por_id(self, usuario_id: int) -> Usuario:
        usuario = await self.session.execute(
            select(Usuario).where(Usuario.id == usuario_id).options(selectinload(Usuario.tarefas))
        )
        return usuario.scalar_one()

    async def buscar_por_email(self, usuario_email: str) -> Usuario | None:
        usuario = await self.session.execute(
            select(Usuario).where(Usuario.email == usuario_email)
        )
        return usuario.scalar_one_or_none()
    
    async def existe_email(self, usuario_email: str) -> str | None:
        email = await self.session.execute(
            select(Usuario.email).where(Usuario.email == usuario_email)
        )
        return email.scalar_one_or_none()

    async def adicionar(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        await self.session.flush()
        await self.session.refresh(usuario)
        return usuario
    
    async def deletar(self, usuario: Usuario) -> None:
        usuario.ativo = False
        usuario.deletado_em = func.now()

    async def recuperar(self, usuario: Usuario) -> Usuario:
        usuario.ativo = True
        usuario.deletado_em = None
        return usuario
    
    async def editar_perfil(self, usuario: Usuario, dados: dict) -> Usuario:
        for campo, valor in dados.items():
            setattr(usuario, campo, valor)
        
        self.session.add(usuario)
        await self.session.flush()
        await self.session.refresh(usuario)
        return await self.buscar_por_id(usuario.id)


    async def editar_senha(self, usuario: Usuario, nova_senha: str) -> None:
        usuario.senha = nova_senha