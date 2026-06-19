from pydantic import BaseModel, Field

from app.core.enums import StatusTarefa


class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str = Field(..., min_length=1)

class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: StatusTarefa

class TarefaUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
