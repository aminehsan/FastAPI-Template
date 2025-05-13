from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.envs import TOKEN
from dependencies import SessionDep
from core.security import create_token
from exceptions import user as user_exceptions
from crud import user as crud_user
from models.models import Token

router = APIRouter(prefix=TOKEN.url, tags=['Login'])


@router.post(path='', response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    db_user = crud_user.authenticate(user_email=form_data.username, user_password=form_data.password, session=session)
    if db_user is None:
        raise user_exceptions.InvalidCredentials()
    if db_user.is_active is False:
        raise user_exceptions.Inactive()
    return Token(
        access_token=create_token(
            str_subject=str(db_user.id),
            expires_seconds=TOKEN.expire
        )
    )
