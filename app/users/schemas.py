from pydantic import BaseModel, EmailStr, constr


class SUser(BaseModel):
    username: constr(min_length=4, max_length=16, strip_whitespace=True)
    email: EmailStr


class SUserCreate(SUser):
    password: constr(min_length=5, max_length=32)


class SUserGet(SUser):
    id: int


class SUserUpdate(SUserCreate):
    username: constr(min_length=4, max_length=16, strip_whitespace=True) | None = None
    email: EmailStr | None = None
    password: constr(min_length=5, max_length=32) | None = None