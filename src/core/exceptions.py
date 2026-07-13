from fastapi import status


class ModelError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        self.message = message

class InvalidCredentialsError(ModelError):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Invalid Token"):
        super().__init__(message)

class AuthorizationError(ModelError):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, message: str = "You don't have authorization for this operation"):
        super().__init__(message)
