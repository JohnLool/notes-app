from app.admin.auth import AdminAuth
from app.config import settings
from app.database import engine
from app.models import UserOrm, NoteOrm
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from starlette.requests import Request


class UserAdmin(ModelView, model=UserOrm):
    column_list = ["id", "username", "email", "is_active", "is_superuser"]
    form_columns = ["username", "email", "hashed_password", "is_active", "is_superuser"]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class NoteAdmin(ModelView, model=NoteOrm):
    column_list = [NoteOrm.id, NoteOrm.title, NoteOrm.user_id, NoteOrm.created_at]
    form_columns = ["title", "description", "user_id", "created_at"]
    name = "Note"
    name_plural = "Notes"
    icon = "fa-solid fa-file"

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


authentication_backend = AdminAuth(secret_key=settings.ADMIN_AUTH_SECRET_KEY)


def setup_admin(app: FastAPI):
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(NoteAdmin)