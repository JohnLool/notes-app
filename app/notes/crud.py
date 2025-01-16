from app.database import session_factory
from app.models import PostOrm
from app.notes.schemas import SPost

from sqlalchemy import select


async def create_post(post: SPost, user_id: int):
    async with session_factory() as session:
        post_to_add = PostOrm(
            title=post.title,
            description=post.description,
            user_id=user_id,
        )

        session.add(post_to_add)
        await session.commit()
        await session.refresh(post_to_add)
        return post_to_add


async def get_all_posts():
    async with session_factory() as session:
        result = await session.execute(select(PostOrm))
        return result.scalars().all()


