import jwt

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from jwt.exceptions import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.core.database import get_async_session


async def decode_access(token: str) -> int:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('sub')
    except DecodeError:
        return 0


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
