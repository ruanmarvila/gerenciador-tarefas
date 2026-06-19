from datetime import datetime, timedelta

from app.core.security import criptografar_senha, verificar_senha
from app.exceptions import CredenciaisInvalidasError, TokenExpiradoError, UsuarioAtivoError
from app.models import Usuario
from app.repositories import UsuarioRepository
from app.schemas import SenhaUpdate, UsuarioLogin, UsuarioUpdate


class UsuarioService:
    def __init__(self, repo: UsuarioRepository) -> None:
        self.repo = repo

    async def perfil(self, usuario_logado: Usuario) -> Usuario:
        usuario = await self.repo.buscar_por_id(usuario_logado.id)
        return usuario
    
    async def editar_perfil(self, usuario_schema: UsuarioUpdate, usuario_logado: Usuario) -> Usuario:
        usuario = await self.repo.buscar_por_id(usuario_logado.id)

        dados = usuario_schema.model_dump()

        return await self.repo.editar_perfil(usuario, dados)
    
    async def editar_senha(self, senha_schema: SenhaUpdate, usuario_logado: Usuario) -> None:
        if senha_schema.senha == senha_schema.nova_senha:
            raise ValueError("A nova senha precisa ser diferente da anterior")
        
        usuario = await self.repo.buscar_por_id(usuario_logado.id)

        if not verificar_senha(senha_schema.senha, usuario.senha):
            raise CredenciaisInvalidasError()
        
        nova_senha_hashed = criptografar_senha(senha_schema.nova_senha)
        await self.repo.editar_senha(usuario, nova_senha_hashed)

    async def deletar_conta(self, usuario_logado: Usuario) -> None:
        usuario = await self.repo.buscar_por_id(usuario_logado.id)
        await self.repo.deletar(usuario)

    async def recuperar_conta(self, usuario_schema: UsuarioLogin) -> Usuario:
        usuario = await self.repo.buscar_por_email(usuario_schema.email)

        if not usuario or not verificar_senha(usuario_schema.senha, usuario.senha):
            raise CredenciaisInvalidasError()
        
        if not usuario.deletado_em:
            raise UsuarioAtivoError()

        if usuario.deletado_em + timedelta(days=30) < datetime.now():
            raise TokenExpiradoError()

        return await self.repo.recuperar(usuario)
