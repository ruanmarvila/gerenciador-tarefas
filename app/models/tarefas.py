from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import StatusTarefa

if TYPE_CHECKING:
    from app.models import Usuario

class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, default="tarefa")
    descricao: Mapped[str] = mapped_column(String(255), nullable=False, default="descrição")
    status: Mapped[StatusTarefa] = mapped_column(
        Enum(StatusTarefa),
        init=False,
        nullable=False, 
        default=StatusTarefa.PENDENTE
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False,
        server_default=text("CURRENT_TIMESTAMP"), 
        nullable=False
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False,
        server_default=text("CURRENT_TIMESTAMP"), 
        onupdate=func.now(), 
        nullable=False
    )
    deletado_em: Mapped[datetime | None] = mapped_column(init=False, nullable=True, default=None)
    usuario: Mapped[Usuario] = relationship(init=False, back_populates="tarefas")