from app.database import session_factory
from app.models import NoteOrm
from app.notes.exception import NoteDoesNotExist, DoNotHaveAccess
from app.notes.schemas import SNote

from sqlalchemy import select


async def create_note(note: SNote, user_id: int):
    async with session_factory() as session:
        note_to_add = NoteOrm(
            title=note.title,
            description=note.description,
            user_id=user_id,
        )

        session.add(note_to_add)
        await session.commit()
        await session.refresh(note_to_add)
        return note_to_add


async def get_all_notes():
    async with session_factory() as session:
        result = await session.execute(select(NoteOrm))
        return result.scalars().all()


async def get_user_notes(user_id: int):
    async with session_factory() as session:
        result = await session.execute(select(NoteOrm).filter(NoteOrm.user_id == user_id))
        return result.scalars().all()


async def get_note_by_id(note_id: int):
    async with session_factory() as session:
        note = await session.get(NoteOrm, note_id)
        if note is None:
            raise NoteDoesNotExist()
        return note


async def update_note(note_id: int, note_new: SNote, user_id: int):
    async with session_factory() as session:
        note_to_update = await session.get(NoteOrm, note_id)
        if note_to_update is None:
            raise NoteDoesNotExist()
        elif note_to_update.user_id != user_id:
            raise DoNotHaveAccess()

        note_to_update.title = note_new.title or note_to_update.title
        note_to_update.description = note_new.description or note_to_update.description
        await session.commit()
        await session.refresh(note_to_update)
        return note_to_update


async def delete_note(note_id: int, user_id: int):
    async with session_factory() as session:
        note_to_delete = await session.get(NoteOrm, note_id)
        if note_to_delete is None:
            raise NoteDoesNotExist()
        elif note_to_delete.user_id != user_id:
            raise DoNotHaveAccess()

        await session.delete(note_to_delete)
        await session.commit()
        return note_to_delete