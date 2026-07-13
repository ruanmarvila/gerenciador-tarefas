from fastapi import status

from src.core.exceptions import ModelError


class PasswordReuseError(ModelError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str = "New password cannot be the same as the current password."):
        super().__init__(message)

class AuthenticationError(ModelError):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message)

class AccountDisabledError(ModelError):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, message: str = "Account disabled. Please reactivate your account."):
        super().__init__(message)

class UserNotFoundError(ModelError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "User not found."):
        super().__init__(message)

class AccountAlreadyActivateError(ModelError):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "Account is already activate."):
        super().__init__(message)

class EmailAlreadyExistsError(ModelError):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "A user with this email already exists."):
        super().__init__(message)
