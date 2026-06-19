from datetime import datetime, timedelta

from app.core.security import criptografar_senha, verificar_senha
from app.exceptions import CredenciaisInvalidasError, EmailDuplicadoError, ModelError
from app.models import Usuario
from app.repositories import UsuarioRepository
from app.schemas import UsuarioCreate


class AuthService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    async def cadastrar_usuario(self, usuario_schema: UsuarioCreate) -> Usuario:
        if await self.repo.existe_email(usuario_schema.email):
            raise EmailDuplicadoError()
        
        hashed_senha = criptografar_senha(usuario_schema.senha)
        novo_usuario = Usuario(nome=usuario_schema.nome,
                               email=usuario_schema.email,
                               senha=hashed_senha)
        
        return await self.repo.adicionar(novo_usuario)
    
    async def login(self, email: str, senha: str) -> Usuario:
        usuario = await self.repo.buscar_por_email(email)

        if not usuario or not verificar_senha(senha, usuario.senha):
            raise CredenciaisInvalidasError()
        
        if usuario.deletado_em and usuario.deletado_em + timedelta(days=30) > datetime.now():
            raise ModelError("Conta desativada. Por favor, reative a sua conta")
        
        return usuario