from typing import List, Annotated, Optional

from app.auth.dependecies import get_current_user, get_optional_user
from app.notes.crud import get_user_notes, get_user_public_notes
from app.notes.schemas import SNoteGet
from app.users.crud import create_user, get_all_users, get_user_by_id, update_user, delete_user
from app.users.exceptions import UsernameAlreadyExists, EmailAlreadyExists, UserDoesNotExist
from app.users.schemas import SUserCreate, SUser, SUserGet, SUserUpdate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{user_id}/notes", response_model=List[SNoteGet])
async def get_user_notes_endpoint(
        user_id: int,
        current_user: Optional[SUserGet] = Depends(get_optional_user)
):
    notes = await get_user_public_notes(user_id)

    if current_user is not None and current_user.id == user_id:
        return RedirectResponse(url="/profile/notes", status_code=307)

    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")
    return notes


@router.post("", response_model=SUser, status_code=201)
async def create_user_endpoint(
        user: SUserCreate,
        current_user: Optional[SUser] = Depends(get_optional_user)
):
    if current_user:
        raise HTTPException(status_code=403, detail="Authorized users cannot create accounts.")
    try:
        return await create_user(user)
    except UsernameAlreadyExists:
        raise HTTPException(status_code=400, detail="Username already exists")
    except EmailAlreadyExists:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("", response_model=List[SUserGet])
async def get_all_users_test_endpoint():
    users = await get_all_users()
    return users


@router.get("/{user_id}", response_model=SUserGet)
async def get_user_by_id_endpoint(user_id: int):
    try:
        return await get_user_by_id(user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")