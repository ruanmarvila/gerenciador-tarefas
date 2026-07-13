from src.core.exceptions import AuthorizationError
from src.tasks.enums import TaskStatus
from src.tasks.exceptions import TaskNotFoundError
from src.tasks.models import Task
from src.tasks.repository import TaskRepository
from src.tasks.schemas import QueryFilter, TaskCreate, TaskUpdate
from src.users.models import User


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    async def create_task(self, task_schema: TaskCreate, current_user: User) -> Task:
        new_task = Task(user_id=current_user.id,
                        title=task_schema.title,
                        description=task_schema.description)
        
        task = await self.repo.add(new_task)
        await self.repo.session.commit()
        return task
    
    async def list_tasks(self, current_user: User, task_filter: QueryFilter) -> list[Task]:
        tasks = await self.repo.get_tasks(current_user.id, task_filter)
        
        if not tasks:
            raise TaskNotFoundError()
        
        return tasks
    
    async def list_deleted_tasks(self, current_user: User) -> list[Task]:
        tasks = await self.repo.get_deleted_tasks(current_user.id)

        if not tasks:
            raise TaskNotFoundError()
        
        return tasks
    
    async def update_task(self, task_id: int, task_schema: TaskUpdate, 
                          current_user: User) -> Task:
        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundError()

        if task.user_id != current_user.id:
            raise AuthorizationError()
        
        datas = task_schema.model_dump(exclude_unset=True)
        
        updated_task = await self.repo.update_task(task, **datas)
        await self.repo.session.commit()
        return updated_task
    
    async def update_status(self, task_id: int, status: TaskStatus, current_user: User) -> Task:
        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundError()
        
        if task.user_id != current_user.id:
            raise AuthorizationError()
        
        updated_task = await self.repo.update_status(task, status)
        await self.repo.session.commit()
        return updated_task
    
    async def delete_task(self, task_id: int, current_user: User) -> Task:
        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundError()
        
        if task.user_id != current_user.id:
            raise AuthorizationError()
        
        deleted_task = await self.repo.soft_delete(task)
        await self.repo.session.commit()
        return deleted_task
    
    async def restore_task(self, task_id: int, current_user: User) -> Task:
        task = await self.repo.get_deleted_tasks_by_id(task_id)

        if not task:
            raise TaskNotFoundError()
        
        if task.user_id != current_user.id:
            raise AuthorizationError()
        
        restored_task = await self.repo.restore(task)
        await self.repo.session.commit()
        return restored_task
    
    async def delete_tasks(self, current_user: User) -> None:
        tasks = await self.repo.get_deleted_tasks(current_user.id)

        if not tasks:
            raise TaskNotFoundError()
        
        for task in tasks:
            await self.repo.delete(task)
        
        await self.repo.session.commit()