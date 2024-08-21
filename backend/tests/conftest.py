"""Setting pytest"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from core import settings
from core.database import get_async_session
from main import app


pytest_plugins = 'tests.fixtures'
engine_test: AsyncEngine = create_async_engine(settings.test_db.async_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Override base async session"""
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
