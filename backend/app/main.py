import asyncio

from app.admin.views import setup_admin
from app.auth.router import router as auth_router
from app.config import settings
from app.database import create_db
from app.notes.router import router as notes_router
from app.users.router import router as users_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

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

app.add_middleware(SessionMiddleware, secret_key=settings.ADMIN_AUTH_SECRET_KEY, max_age=300)


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())