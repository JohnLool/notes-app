from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    username: str
    email: EmailStr

class SUserCreate(SUser):
    password: str

class SUserGet(SUser):
    id: int

class SUserUpdate(SUserCreate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None