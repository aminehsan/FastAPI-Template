from abc import ABC
from fastapi import HTTPException, status


class ItemHTTPException(HTTPException, ABC):
    status_code: int
    detail: str

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class NotFound(ItemHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Item not found.'


class PermissionDenied(ItemHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Not enough permissions.'
