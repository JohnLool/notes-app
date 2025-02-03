from fastapi import APIRouter, Depends, HTTPException
from app.notes.crud import get_all_public_notes


router = APIRouter()


@router.get("/feed")
async def get_feed():
    feed = await get_all_public_notes()
    return feed