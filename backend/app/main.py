from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.admin.views import setup_admin
from app.config import settings
from app.database import create_db

from app.users.user_profile.router import router as user_profile_router
from app.feed.router import router as feed_router
from app.auth.router import router as auth_router
from app.notes.router import router as notes_router
from app.users.router import router as users_router
from app.cache import init_cache

import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_db()
    # await init_cache()
    yield


app = FastAPI(lifespan=lifespan)
logger.info("Приложение запущено!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(app)
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(auth_router)
app.include_router(feed_router)
app.include_router(user_profile_router)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.ADMIN_AUTH_SECRET_KEY,
    max_age=300
)