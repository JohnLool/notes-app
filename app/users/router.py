from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.users.crud import create_user, get_all_users, get_user_by_id, update_user, delete_user
from app.users.exceptions import UsernameAlreadyExists, EmailAlreadyExists, UserDoesNotExist
from app.users.schemas import SUserCreate, SUser, SUserGet, SUserUpdate
from app.auth.dependecies import get_current_user, get_optional_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/me", response_model=SUserGet)
async def read_users_me(current_user: Annotated[SUserGet, Depends(get_current_user)]):
    return current_user


@router.post("/", response_model=SUser, status_code=201)
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


@router.get("/", response_model=List[SUserGet])
async def get_all_users_endpoint():
    users = await get_all_users()
    return users


@router.get("/{user_id}/", response_model=SUserGet)
async def get_user_by_id_endpoint(user_id: int):
    try:
        return await get_user_by_id(user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/me", response_model=SUserUpdate)
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


@router.delete("/me", status_code=204)
async def delete_current_user_endpoint(current_user: Annotated[SUserGet, Depends(get_current_user)]):
    await delete_user(current_user.id)