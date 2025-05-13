from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Query, status
from dependencies import SessionDep, CurrentUser
from crud import item as item_crud
from exceptions import item as item_exceptions
from models.models import Message
from models.items import ItemCreate, ItemUpdate, ItemShow

router = APIRouter(prefix='/items', tags=['items'])


@router.post(path='', status_code=status.HTTP_201_CREATED, response_model=Message)
def create(current_user: CurrentUser, item: ItemCreate, session: SessionDep):
    item_crud.create(owner_id=current_user.id, item=item, session=session)
    return Message(message='Item created successfully.')


@router.get(path='', response_model=list[ItemShow])
def read(session: SessionDep, skip: Annotated[int, Query(ge=0)], limit: Annotated[int, Query(ge=1, le=100)]):
    return item_crud.read(skip=skip, limit=limit, session=session)


@router.get(path='/{item_id}', response_model=ItemShow)
def read_by_id(item_id: UUID, session: SessionDep):
    db_item = item_crud.read_by_id(item_id=item_id, session=session)
    if db_item is None:
        raise item_exceptions.NotFound()
    return db_item


@router.put(path='/{item_id}', response_model=Message)
def update(current_user: CurrentUser, item_id: UUID, item: ItemUpdate, session: SessionDep):
    db_item = item_crud.read_by_id(item_id=item_id, session=session)
    if db_item is None:
        raise item_exceptions.NotFound()
    if current_user.has_item_permission(db_item) is False:
        raise item_exceptions.PermissionDenied()
    item_crud.update(db_item=db_item, item=item, session=session)
    return Message(message='Item updated successfully.')


@router.delete(path='/{item_id}', response_model=Message)
def delete(current_user: CurrentUser, item_id: UUID, session: SessionDep):
    db_item = item_crud.read_by_id(item_id=item_id, session=session)
    if db_item is None:
        raise item_exceptions.NotFound()
    if current_user.has_item_permission(db_item) is False:
        raise item_exceptions.PermissionDenied()
    item_crud.delete(db_item=db_item, session=session)
    return Message(message='Item deleted successfully.')
