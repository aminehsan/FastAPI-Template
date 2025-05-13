from typing import Annotated
from pydantic import ValidationError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jwt.exceptions import InvalidTokenError
from exceptions import user as user_exceptions
from crud import user as crud_user
from core.envs import TOKEN
from core.security import read_token
from core.database import engine
from models.users import User
from models.models import TokenPayload


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(TOKEN.url))]


def read_current_user(token: TokenDep, session: SessionDep) -> User:
    try:
        token_data = TokenPayload(**read_token(token))
    except (InvalidTokenError, ValidationError):
        raise user_exceptions.InvalidToken()
    db_user = crud_user.read_by_id(user_id=token_data.sub, session=session)
    if db_user is None:
        raise user_exceptions.NotFound()
    if db_user.is_active is False:
        raise user_exceptions.Inactive()
    return db_user


CurrentUser = Annotated[User, Depends(read_current_user)]


def require_superuser(current_user: CurrentUser):
    if current_user.is_superuser is False:
        raise user_exceptions.InsufficientPermissions()
