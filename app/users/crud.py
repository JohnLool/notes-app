from fastapi import HTTPException, status
from sqlalchemy import select

from app.database import session_factory
from app.models import UserOrm
from app.users.schemas import SUserCreate, SUserUpdate
from app.utils import hash_password


async def create_user(user: SUserCreate):
    async with session_factory() as session:
        user_to_add = UserOrm(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        session.add(user_to_add)
        await session.commit()
        await session.refresh(user_to_add)
        return user_to_add


async def get_user_by_id(user_id: int):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )
        return user


async def get_all_users():
    async with session_factory() as session:
        result = await session.execute(select(UserOrm))
        return result.scalars().all()


async def get_user_by_username(username: str):
    async with session_factory() as session:
        result = await session.execute(select(UserOrm).filter(UserOrm.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found"
            )
        return user


async def update_user(user_id: int, user_data: SUserUpdate):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found")
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.password = user_data.password or user.password
        await session.commit()
        await session.refresh(user)
        return user


async def delete_user(user_id: int):
    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found")
        await session.delete(user)
        await session.commit()
        return user