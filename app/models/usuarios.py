from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models import Tarefa

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True, init=False)
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
    tarefas: Mapped[list[Tarefa]] = relationship(
        init=False,
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
