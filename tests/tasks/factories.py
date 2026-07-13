import factory

from src.tasks.models import Task


class TaskFactory(factory.Factory): # type: ignore
    class Meta:
        model = Task

    title = factory.Faker("text") # type: ignore
    description = factory.Faker("text") # type: ignore
    user_id = 1