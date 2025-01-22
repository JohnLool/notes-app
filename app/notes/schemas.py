from pydantic import BaseModel, constr


class SNote(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: constr(min_length=1, max_length=255)


class SNoteGet(SNote):
    id: int
    user_id: int


class SNoteUpdate(SNote):
    title: constr(min_length=1, max_length=255) | None = None
    description: constr(min_length=1, max_length=255) | None = None