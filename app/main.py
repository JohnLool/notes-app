import asyncio

from fastapi import FastAPI

from app.database import create_db
from app.users.router import router as users_router
from app.notes.router import router as notes_router
app = FastAPI()

app.include_router(users_router)
app.include_router(notes_router)


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())