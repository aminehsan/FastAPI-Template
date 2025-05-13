from re import match
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship
from exceptions import user as user_exceptions
from core.envs import PASSWORD_PATTERN

if TYPE_CHECKING:
    from .items import Item


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, min_length=10, max_length=70)
    full_name: str = Field(min_length=5, max_length=30)
    age: int = Field(ge=5, le=120)


class User(UserBase, table=True):
    __tablename__ = 'users'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    is_superuser: bool = False
    is_active: bool = True
    hashed_password: str = Field(max_length=256)
    items: list['Item'] = Relationship(back_populates='owner', cascade_delete=True)

    def has_item_permission(self, item: 'Item') -> bool:
        return self.is_superuser or item.is_owned_by(self)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if not match(PASSWORD_PATTERN, value):
            raise user_exceptions.InvalidPasswordPattern()
        return value


class UserUpdate(UserCreate):
    new_password: str | None = Field(default=None, min_length=8, max_length=20)

    @field_validator('new_password')
    def validate_password(cls, value: str) -> str:
        if not match(PASSWORD_PATTERN, value):
            raise user_exceptions.InvalidPasswordPattern()
        return value


class UserDelete(SQLModel):
    password: str = Field(min_length=8, max_length=20)


class UserShow(UserBase):
    id: UUID
    is_superuser: bool
    is_active: bool
