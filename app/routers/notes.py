from fastapi import APIRouter, Depends

from app.crud import create_user
from app.schemas import SUserCreate, SUser

router = APIRouter()


@router.post("/users/", response_model=SUser, status_code=201)
async def create_user_endpoint(user: SUserCreate):
    user_to_add = await create_user(user)
    return user_to_add