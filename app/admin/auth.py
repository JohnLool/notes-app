from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.users.crud import get_user_by_username
from app.utils import verify_password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await get_user_by_username(username)

        if user and verify_password(password, user.hashed_password) and user.is_superuser:
            request.session["logged_in"] = True
            return True
        return False


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True


    async def authenticate(self, request: Request) -> bool:
        if request.session.get("logged_in"):
            return True
        return False
