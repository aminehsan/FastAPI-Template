from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt import encode, decode
from .envs import CRYPT_CONTEXT_SCHEME, TOKEN, FASTAPI

pwd_context = CryptContext(schemes=[CRYPT_CONTEXT_SCHEME], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(str_subject: str, expires_seconds: int) -> str:
    return encode(
        payload={
            'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_seconds),
            'sub': str_subject
        },
        key=FASTAPI.secret_key,
        algorithm=TOKEN.algorithm
    )


def read_token(token: str) -> dict:
    return decode(
        jwt=token,
        key=FASTAPI.secret_key,
        algorithms=[TOKEN.algorithm]
    )
