from pydantic import BaseModel, Field

from src.tasks.enums import TaskColumn, TaskOrder, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(default="Title", min_length=1)
    description: str = Field(default="Description", min_length=1)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)


class Pagination(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class TaskFilter(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = Field(default=None, min_length=3)
    status: TaskStatus | None = None


class OrderFilter(BaseModel):
    column: TaskColumn | None = None
    order: TaskOrder | None = None


class QueryFilter(Pagination, TaskFilter, OrderFilter):
    pass