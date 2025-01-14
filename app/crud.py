from app.database import session_factory
from app.models import UserOrm
from app.schemas import SUserCreate
from app.utils import hash_password


async def create_user(user: SUserCreate):
    async with session_factory() as session:
        user_to_add = UserOrm(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        session.add(user_to_add)
        await session.commit()
        await session.refresh(user_to_add)
        return user_to_add