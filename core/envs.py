from re import match
from pydantic_settings import BaseSettings
from pydantic import Field, EmailStr, field_validator, computed_field
from exceptions import user as user_exceptions

CRYPT_CONTEXT_SCHEME: str = 'bcrypt'
SECRET_KEY_PATTERN: str = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
PASSWORD_PATTERN: str = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).+$'


class TokenSettings(BaseSettings):
    algorithm: str = 'HS256'
    url: str = '/login'
    expire: int = 60 * 60 * 24 * 2  # 2 days

    model_config = {'env_file': None}


class FastapiSettings(BaseSettings):
    title: str
    port: int
    allow_origins: list[str]
    secret_key: str = Field(min_length=30)
    create_database: bool
    run_development: bool

    @field_validator('secret_key')
    def validate_secret_key(cls, value: str) -> str:
        if not match(SECRET_KEY_PATTERN, value):
            raise ValueError('Secret key must include lowercase, uppercase and digit.')
        return value

    @computed_field
    @property
    def workers(self) -> int | None:
        if self.run_development is False:
            # return 4
            return None

    @computed_field
    @property
    def reload(self) -> bool:
        # return self.run_development
        return False

    model_config = {
        'env_prefix': 'FASTAPI_',
        'extra': 'forbid'
    }


class SuperuserSettings(BaseSettings):
    email: EmailStr = Field(max_length=70)
    full_name: str = Field(min_length=6, max_length=30)
    age: int = Field(ge=5, le=150)
    password: str = Field(min_length=8, max_length=20)

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if not match(PASSWORD_PATTERN, value):
            raise user_exceptions.InvalidPasswordPattern()
        return value

    model_config = {
        'env_prefix': 'SUPERUSER_',
        'extra': 'forbid'
    }


class PostgresSettings(BaseSettings):
    host: str
    port: int
    db: str
    user: str
    password: str

    @computed_field
    @property
    def url(self) -> str:
        host = 'localhost' if FastapiSettings().run_development else self.host
        return f'postgresql+psycopg://{self.user}:{self.password}@{host}:{self.port}/{self.db}'

    model_config = {
        'env_prefix': 'POSTGRES_',
        'extra': 'forbid'
    }


TOKEN = TokenSettings()
FASTAPI = FastapiSettings()
SUPERUSER = SuperuserSettings()
POSTGRES = PostgresSettings()
