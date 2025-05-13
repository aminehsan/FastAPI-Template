from sqlmodel import SQLModel, Session, create_engine
from .envs import POSTGRES, SUPERUSER
from crud import user as user_crud

engine = create_engine(POSTGRES.url)


def create_database_and_tables():
    print('Creating database and tables...')
    SQLModel.metadata.create_all(engine)


def create_superuser():
    print('Creating superuser...')
    with Session(engine) as session:
        if user_crud.read_by_email(user_email=SUPERUSER.email, session=session) is None:
            user_crud.create(user=SUPERUSER, session=session, is_superuser=True)


def delete_database_and_tables():
    print('Deleting database and tables...')
    SQLModel.metadata.drop_all(engine)
