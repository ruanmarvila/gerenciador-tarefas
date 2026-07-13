from typing import Annotated

from fastapi import APIRouter, Query, status

from src.tasks.dependencies import TaskServiceDep
from src.tasks.enums import TaskStatus
from src.tasks.schemas import QueryFilter, TaskCreate, TaskResponse, TaskUpdate
from src.users.dependencies import CurrentUserDep

router = APIRouter(
    prefix="/api/v1/tasks", 
    tags=["tasks"]
)

@router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create(task_schema: TaskCreate, current_user: CurrentUserDep, service: TaskServiceDep):
    return await service.create_task(task_schema, current_user)

@router.get("/list", response_model=list[TaskResponse])
async def list_tasks(current_user: CurrentUserDep, task_filter: Annotated[QueryFilter, Query()], 
               service: TaskServiceDep):
    return await service.list_tasks(current_user, task_filter)

@router.patch("/update/{task_id}", response_model=TaskResponse)
async def update(task_id: int, task_schema: TaskUpdate, current_user: CurrentUserDep, 
                 service: TaskServiceDep):
    return await service.update_task(task_id, task_schema, current_user)

@router.patch("/update/status/{task_id}", response_model=TaskResponse)
async def update_status(task_id: int, status: TaskStatus, current_user: CurrentUserDep, 
                   service: TaskServiceDep):
    return await service.update_status(task_id, status, current_user)

@router.get("/bin", response_model=list[TaskResponse])
async def bin(current_user: CurrentUserDep, service: TaskServiceDep):
    return await service.list_deleted_tasks(current_user)

@router.delete("/delete/bin", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bin(current_user: CurrentUserDep, service: TaskServiceDep):
    await service.delete_tasks(current_user)

@router.delete("/delete/{task_id}", response_model=TaskResponse)
async def delete(task_id: int, current_user: CurrentUserDep, service: TaskServiceDep):
    return await service.delete_task(task_id, current_user)

@router.patch("/restore/{task_id}", response_model=TaskResponse)
async def restore(task_id: int, current_user: CurrentUserDep, service: TaskServiceDep):
    return await service.restore_task(task_id, current_user)