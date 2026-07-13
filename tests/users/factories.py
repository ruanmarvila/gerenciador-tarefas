import factory

from src.users.models import User


class UserFactory(factory.Factory):  # type: ignore
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f"test{n}") # type: ignore
    email = factory.LazyAttribute(lambda obj: f"{obj.name}@test.com") # type: ignore
    password = factory.LazyAttribute(lambda obj: f"{obj.name}example") # type: ignore