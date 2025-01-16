from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.notes.exception import DoNotHaveAccess, NoteDoesNotExist
from app.notes.schemas import SNote, SNoteGet, SNoteUpdate
from app.notes.crud import create_note, get_all_notes, update_note, delete_note, get_note_by_id

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=SNote, status_code=201)
async def create_note_endpoint(note: SNote, current_user_id: int):
    return await create_note(note, current_user_id)


@router.get("/", response_model=List[SNoteGet])
async def get_all_notes_endpoint():
    return await get_all_notes()


@router.get("/{note_id}", response_model=SNoteGet)
async def get_note_by_id_endpoint(note_id: int):
    try:
        return await get_note_by_id(note_id)
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")


@router.put("/{note_id}", status_code=204)
async def update_note_endpoint(note_id: int, note_new: SNoteUpdate, user_id: int):
    try:
        return await update_note(note_id, note_new, user_id)
    except DoNotHaveAccess:
        raise HTTPException(status_code=403, detail="Access Denied")
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}", status_code=204)
async def delete_note_endpoint(note_id: int, user_id: int):
    try:
        return await delete_note(note_id, user_id)
    except DoNotHaveAccess:
        raise HTTPException(status_code=403, detail="Access Denied")
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")