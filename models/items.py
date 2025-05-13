from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .users import User


class ItemBase(SQLModel):
    title: str = Field(min_length=5, max_length=70)
    description: str = Field(min_length=10, max_length=200)


class Item(ItemBase, table=True):
    __tablename__ = 'items'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    is_active: bool = True
    owner_id: UUID = Field(foreign_key='users.id', nullable=False, ondelete='CASCADE')
    owner: Optional['User'] = Relationship(back_populates='items')

    def is_owned_by(self, user: 'User') -> bool:
        return self.owner_id == user.id


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemCreate):
    pass


class ItemShow(ItemBase):
    id: UUID
    is_active: bool
    owner_id: UUID
