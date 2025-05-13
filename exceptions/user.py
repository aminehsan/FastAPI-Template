from abc import ABC
from fastapi import HTTPException, status


# HTTP Exception
class UserHTTPException(HTTPException, ABC):
    status_code: int
    detail: str

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFound(UserHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found.'


class DuplicateEmail(UserHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Email already exists.'


class InvalidPassword(UserHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Incorrect password.'


class InvalidCredentials(UserHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Incorrect email or password.'


class DeleteForbidden(UserHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'You are not allowed to delete this user.'


class Inactive(UserHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Inactive user.'


class InvalidToken(UserHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Could not validate credentials.'


class InsufficientPermissions(UserHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "The user doesn't have enough permissions."


# Value Exception
class UserValueException(ValueError, ABC):
    detail: str

    def __init__(self) -> None:
        super().__init__(self.detail)


class InvalidPasswordPattern(UserValueException):
    detail = 'Password must include lowercase, uppercase, digit and special char.'
