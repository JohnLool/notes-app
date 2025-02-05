from typing import Annotated, List

from app.auth.dependecies import get_current_user, get_optional_user
from app.notes.crud import create_note, get_all_notes, update_note, delete_note, get_note_by_id, get_user_notes
from app.notes.exception import DoNotHaveAccess, NoteDoesNotExist
from app.notes.schemas import SNote, SNoteGet, SNoteUpdate
from app.users.schemas import SUserGet
from fastapi import APIRouter, Depends, HTTPException


import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=SNoteGet, status_code=201)
async def create_note_endpoint(note: SNote, current_user: Annotated[SUserGet, Depends(get_current_user)]):
    return await create_note(note, current_user.id)


@router.get("", response_model=List[SNoteGet])
async def get_notes_test_endpoint():
    return await get_all_notes()


@router.get("/{note_id}", response_model=SNoteGet)
async def get_note_by_id_endpoint(note_id: int):
    try:
        return await get_note_by_id(note_id)
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")