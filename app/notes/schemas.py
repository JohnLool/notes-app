from pydantic import BaseModel


class SNote(BaseModel):
    title: str
    description: str


class SNoteGet(SNote):
    id: int


class SNoteUpdate(SNote):
    title: str | None = None
    description: str | None = None