from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_access_token
from fastapi import Depends, HTTPException, status

from typing import Annotated

from app.users.crud import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str,  Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
