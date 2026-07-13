from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.tasks.enums import TaskStatus

if TYPE_CHECKING:
    from src.users.models import User

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="title")
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="description")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        init=False,
        nullable=False, 
        default=TaskStatus.TODO
    )
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
    user: Mapped[User] = relationship(init=False, back_populates="tasks")