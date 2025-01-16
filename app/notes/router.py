from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.notes.schemas import SPost, SPostGet
from app.notes.crud import create_post, get_all_posts

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=SPost, status_code=201)
async def create_post_endpoint(post: SPost, current_user_id: int):
    return await create_post(post, current_user_id)


@router.get("/", response_model=List[SPostGet])
async def get_all_posts_endpoint():
    return await get_all_posts()