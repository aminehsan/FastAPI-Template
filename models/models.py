from uuid import UUID
from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(SQLModel):
    sub: UUID


class Message(SQLModel):
    message: str
