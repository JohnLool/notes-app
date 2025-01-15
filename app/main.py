import asyncio

from fastapi import FastAPI

from app.database import create_db
from app.users.router import router

app = FastAPI()

app.include_router(router)


async def main():
    await create_db()


if __name__ == "__main__":
    asyncio.run(main())