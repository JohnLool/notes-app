import asyncio

from fastapi import FastAPI

from app.database import create_db
from app.routers import users

app = FastAPI()

app.include_router(users.router)


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())