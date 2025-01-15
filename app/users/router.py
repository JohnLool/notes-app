from typing import List

from fastapi import APIRouter, Depends

from app.users.crud import create_user, get_all_users, get_user_by_id, update_user
from app.users.schemas import SUserCreate, SUser, SUserGet, SUserUpdate

router = APIRouter()


@router.post("/users/", response_model=SUser, status_code=201)
async def add_user_endpoint(user: SUserCreate):
    user_to_add = await create_user(user)
    return user_to_add

@router.get("/users/", response_model=List[SUserGet])
async def get_all_users_endpoint():
    users = await get_all_users()
    return users

@router.get("/users/{user_id}/", response_model=SUserGet)
async def get_user_by_id_endpoint(user_id: int):
    user = await get_user_by_id(user_id)
    return user

@router.put("/users/{user_id}/", response_model=SUserUpdate)
async def update_user_endpoint(user_id: int, user_data: SUserUpdate):
    user = await update_user(user_id, user_data)
    return user