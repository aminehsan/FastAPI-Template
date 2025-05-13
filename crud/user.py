from uuid import UUID
from pydantic import EmailStr
from sqlmodel import Session, select
from core.security import hash_password, verify_password
from models.users import User, UserCreate, UserUpdate


def create(user: UserCreate, session: Session, is_superuser: bool = False):
    session.add(User.model_validate(
        user,
        update={
            'is_superuser': is_superuser,
            'hashed_password': hash_password(user.password)
        }
    ))
    session.commit()


def read_by_id(user_id: UUID, session: Session) -> User | None:
    return session.get(User, user_id)


def read_by_email(user_email: EmailStr, session: Session) -> User | None:
    return session.exec(
        statement=select(User).where(User.email == user_email)
    ).first()


def read(skip: int, limit: int, session: Session) -> list[User]:
    return session.exec(
        statement=select(User).offset(skip).limit(limit)
    ).all()


def update(db_user: User, user: UserUpdate, session: Session):
    db_user.sqlmodel_update(user.model_dump(exclude_unset=True))
    if user.new_password:
        db_user.hashed_password = hash_password(user.new_password)
    session.add(db_user)
    session.commit()


def delete(db_user: User, session: Session):
    session.delete(db_user)
    session.commit()


def authenticate(user_email: EmailStr, user_password: str, session: Session) -> User | None:
    db_user = read_by_email(user_email=user_email, session=session)
    if db_user and verify_password(user_password, db_user.hashed_password):
        return db_user
