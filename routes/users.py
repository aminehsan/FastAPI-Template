from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from dependencies import SessionDep, CurrentUser, require_superuser
from core.security import verify_password
from exceptions import user as user_exceptions
from crud import user as crud_user
from models.users import UserCreate, UserUpdate, UserShow, UserDelete
from models.models import Message

router = APIRouter(prefix='/users', tags=['Users'])


@router.post(path='', status_code=status.HTTP_201_CREATED, response_model=Message)
def create(user: UserCreate, session: SessionDep):
    if crud_user.read_by_email(user_email=user.email, session=session):
        raise user_exceptions.DuplicateEmail()
    crud_user.create(user=user, session=session)
    return Message(message='User created successfully.')


@router.get(path='', dependencies=[Depends(require_superuser)], response_model=list[UserShow])
def read(session: SessionDep, skip: Annotated[int, Query(ge=0)], limit: Annotated[int, Query(ge=1, le=100)]):
    return crud_user.read(skip=skip, limit=limit, session=session)


@router.get(path='/me', response_model=UserShow)
def read(current_user: CurrentUser):
    return current_user


@router.put(path='/me', response_model=Message)
def update(current_user: CurrentUser, user: UserUpdate, session: SessionDep):
    if verify_password(plain_password=user.password, hashed_password=current_user.hashed_password) is False:
        raise user_exceptions.InvalidPassword()
    if (user.email != current_user.email) and crud_user.read_by_email(user_email=user.email, session=session):
        raise user_exceptions.DuplicateEmail()
    crud_user.update(db_user=current_user, user=user, session=session)
    return Message(message='User updated successfully.')


@router.delete(path='/me', response_model=Message)
def delete(current_user: CurrentUser, user: UserDelete, session: SessionDep):
    if verify_password(plain_password=user.password, hashed_password=current_user.hashed_password) is False:
        raise user_exceptions.InvalidPassword()
    if current_user.is_superuser:
        raise user_exceptions.DeleteForbidden()
    crud_user.delete(db_user=current_user, session=session)
    return Message(message='User deleted successfully.')


@router.get(path='/{user_id}', response_model=UserShow)
def read_by_id(user_id: UUID, session: SessionDep):
    db_user = crud_user.read_by_id(user_id=user_id, session=session)
    if db_user is None:
        raise user_exceptions.NotFound()
    return db_user
