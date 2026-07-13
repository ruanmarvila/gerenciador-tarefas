from typing import Annotated

from fastapi import Depends

from src.core.database import DBSession
from src.tasks.repository import TaskRepository
from src.tasks.service import TaskService


def get_task_repository(session: DBSession) -> TaskRepository:
    return TaskRepository(session)

TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]


def get_task_service(repo: TaskRepositoryDep) -> TaskService:
    return TaskService(repo)

TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]