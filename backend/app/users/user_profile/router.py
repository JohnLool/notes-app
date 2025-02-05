from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated

from app.auth.dependecies import get_current_user
from app.notes.crud import get_user_notes, delete_note, update_note
from app.notes.exception import DoNotHaveAccess, NoteDoesNotExist
from app.notes.schemas import SNoteGet, SNoteUpdate
from app.users.crud import update_user, delete_user
from app.users.exceptions import EmailAlreadyExists, UsernameAlreadyExists
from app.users.schemas import SUserGet, SUserUpdate

router = APIRouter(
    prefix="/me",
    tags=["user_profile"],
)


@router.get("", response_model=SUserGet)
async def read_users_me(current_user: Annotated[SUserGet, Depends(get_current_user)]):
    return current_user


@router.get("/notes", response_model=List[SNoteGet])
async def get_user_notes_endpoint(current_user: Annotated[SUserGet, Depends(get_current_user)]):
    notes = await get_user_notes(current_user.id)
    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")
    return notes

@router.put("", response_model=SUserUpdate)
async def update_current_user_endpoint(
    user_data: SUserUpdate,
    current_user: Annotated[SUserGet, Depends(get_current_user)]
):
    try:
        return await update_user(current_user.id, user_data)
    except EmailAlreadyExists:
        raise HTTPException(status_code=400, detail="Email already exists")
    except UsernameAlreadyExists:
        raise HTTPException(status_code=400, detail="Username already exists")


@router.delete("", status_code=204)
async def delete_current_user_endpoint(current_user: Annotated[SUserGet, Depends(get_current_user)]):
    await delete_user(current_user.id)


@router.put("/notes/{note_id}", response_model=SNoteGet, status_code=201)
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


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note_endpoint(
        note_id: int,
        current_user: Annotated[SUserGet, Depends(get_current_user)]
):
    try:
        return await delete_note(note_id, current_user.id)
    except DoNotHaveAccess:
        raise HTTPException(status_code=403, detail="Access Denied")
    except NoteDoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")