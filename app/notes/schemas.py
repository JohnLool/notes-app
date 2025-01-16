from pydantic import BaseModel


class SPost(BaseModel):
    title: str
    description: str


class SPostGet(SPost):
    id: int


class SPostUpdate(SPost):
    title: str | None = None
    description: str | None = None