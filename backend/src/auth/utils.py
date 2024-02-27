from auth.models import User
from config import SECRET_AUTH
from db.database import get_async_session
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession


async def decode_access(token: str) -> int:
    """Decode access token if valid"""
    try:
        payload = jwt.decode(token, key=SECRET_AUTH, algorithms=['HS256'], audience='fastapi-users:auth')
        return payload.get('sub')
    except JWTError:
        return 0


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
