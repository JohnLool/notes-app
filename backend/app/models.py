from datetime import datetime
from typing import Annotated

from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

intpk = Annotated[int, mapped_column(Integer, primary_key=True)]

Base = declarative_base()

class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

class NoteOrm(Base):
    __tablename__ = "notes"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())