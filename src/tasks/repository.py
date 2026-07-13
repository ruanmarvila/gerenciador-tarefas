from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.tasks.enums import TaskOrder, TaskStatus
from src.tasks.models import Task
from src.tasks.schemas import QueryFilter


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_tasks(self, user_id: int, filters: QueryFilter) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id, Task.deleted_at.is_(None))

        if filters.title is not None:
            query = query.where(Task.title.ilike(f"%{filters.title}%"))

        if filters.description is not None:
            query = query.where(Task.description.ilike(f"%{filters.description}%"))

        if filters.status is not None:
            query = query.where(Task.status == filters.status)

        if filters.column is not None:
            column = getattr(Task, filters.column.value)

            if filters.order == TaskOrder.DESCENDING:
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())

        query = query.offset(filters.offset).limit(filters.limit)

        tasks = await self.session.execute(query)

        return list(tasks.scalars().all())
    
    async def get_by_id(self, Task_id: int) -> Task | None:
        task = await self.session.execute(
            select(Task).where(Task.id == Task_id, 
                               Task.deleted_at.is_(None))
        )
        return task.scalar_one_or_none()
    
    async def get_deleted_tasks(self, user_id: int) -> list[Task]:
        tasks = await self.session.execute(
            select(Task).where(Task.user_id == user_id, 
                                 Task.deleted_at.is_not(None))
        )
        return list(tasks.scalars().all())

    async def get_deleted_tasks_by_id(self, Task_id: int) -> Task | None:
        task = await self.session.execute(
            select(Task).where(Task.id == Task_id, 
                               Task.deleted_at.is_not(None))
        )
        return task.scalar_one_or_none()
    
    async def update_status(self, task: Task, status: TaskStatus):
        task.status = status
        await self.session.flush()
        await self.session.refresh(task)
        return task
    
    async def update_task(self, task: Task, **datas) -> Task:
        for field, value in datas.items():
            if value is not None:
                setattr(task, field, value)

        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task
    
    async def soft_delete(self, task: Task) -> Task:
        task.deleted_at = func.now()
        return task
    
    async def restore(self, task: Task) -> Task:
        task.deleted_at = None
        return task

    async def add(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task
    
    async def delete(self, task: Task) -> None:
        await self.session.delete(task)