from typing import Annotated, List

from app.auth.dependecies import get_current_user, get_optional_user
from app.notes.crud import create_note, get_all_notes, update_note, delete_note, get_note_by_id, get_user_notes
from app.notes.exception import DoNotHaveAccess, NoteDoesNotExist
from app.notes.schemas import SNote, SNoteGet, SNoteUpdate
from app.users.schemas import SUserGet
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=SNote, status_code=201)
async def create_note_endpoint(note: SNote, current_user: Annotated[SUserGet, Depends(get_current_user)]):
    return await create_note(note, current_user.id)


@router.get("", response_model=List[SNoteGet])
@cache(expire=300)
async def get_notes_endpoint(
        current_user: Annotated[SUserGet, Depends(get_optional_user)],
        owner: str = None
):
    if owner == 'me' and current_user is not None:
        return await get_user_notes(current_user.id)
    elif owner is None:
        return await get_all_notes()
    elif owner.isdigit():
        return await get_user_notes(int(owner))
    else:
        return await get_all_notes()


@router.get("/{note_id}", response_model=SNoteGet)
async def get_note_by_id_endpoint(note_id: int):
    try:
        return await get_note_by_id(note_id)
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")


@router.put("/{note_id}", response_model=SNoteGet, status_code=201)
async def update_note_endpoint(
        note_id: int,
        note_new: SNoteUpdate,
        current_user: Annotated[SUserGet, Depends(get_current_user)]
):
    try:
        return await update_note(note_id, note_new, current_user.id)
    except DoNotHaveAccess:
        raise HTTPException(status_code=403, detail="Access Denied")
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}", status_code=204)
async def delete_note_endpoint(note_id: int,
                               current_user: Annotated[SUserGet, Depends(get_current_user)]
                               ):
    try:
        return await delete_note(note_id, current_user.id)
    except DoNotHaveAccess:
        raise HTTPException(status_code=403, detail="Access Denied")
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")