from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas import TarefaResponse


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr
    senha: str = Field(..., min_length=3)

    @field_validator('nome', 'senha')
    @classmethod
    def verificar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=1)
    
    @field_validator('senha')
    @classmethod
    def verificar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()
    
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None

    class Config:
        from_attributes = True

class SenhaUpdate(BaseModel):
    senha: str
    nova_senha: str

    @field_validator('senha', 'nova_senha')
    @classmethod
    def verificar_vazios(cls, valor: str):
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()
    
    class Config:
        from_attributes = True

class UsuarioResponse(BaseModel):
    id: int
    nome: str

class PerfilResponse(BaseModel):
    id: int
    nome: str
    tarefas: list[TarefaResponse] = []
