from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.tasks.models import Task

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=text("CURRENT_TIMESTAMP"), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=text("CURRENT_TIMESTAMP"), 
        onupdate=func.now(),
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(init=False, nullable=True, default=None)
    tasks: Mapped[list[Task]] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
