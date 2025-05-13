from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.envs import FASTAPI
from core.database import create_database_and_tables, create_superuser, delete_database_and_tables
from routes.users import router as users_router
from routes.login import router as login_router
from routes.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if FASTAPI.create_database:
        create_database_and_tables()
        create_superuser()
    yield
    if FASTAPI.create_database and FASTAPI.run_development:
        delete_database_and_tables()


app = FastAPI(title=FASTAPI.title, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FASTAPI.allow_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(users_router)
app.include_router(login_router)
app.include_router(items_router)
