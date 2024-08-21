from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.auth.models import User
from src.auth.utils import get_user_db
from src.core.settings import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.app.secret_auth
    verification_token_secret = settings.app.secret_auth


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
