from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from app.auth.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.users.crud import get_user_by_email
from app.utils import verify_password
from app.auth.jwt import create_access_token

from app.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


