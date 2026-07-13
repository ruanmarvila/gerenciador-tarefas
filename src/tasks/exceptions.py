from fastapi import status

from src.core.exceptions import ModelError


class TaskNotFoundError(ModelError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "Task not found"):
        super().__init__(message)