"""
Pytest fixtures
"""
from typing import AsyncGenerator

import pytest
from conftest import async_session_maker, engine_test
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from auth.models import User
from core.database import Base
from tests.factories import UserFactory


@pytest.fixture
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session use async session maker"""
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator:
    """
    Create tables after connect to database
    Drop tables before end tests
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def not_auth_user_client() -> AsyncGenerator[AsyncClient, None]:
    """Return async generator async client"""
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
async def auth_user_client(creata_new_user_with_token: str):
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers={"Authorization": f"Bearer {creata_new_user_with_token}"}
    ) as ac:
        yield ac


@pytest.fixture
def user_data_register() -> dict:
    return {
        "email": "tsp7439@gmail.com",
        "password": "1234",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "test username",
    }


@pytest.fixture
def user_data_login() -> dict:
    return {
        "username": "tsp7439@gmail.com",
        "password": "1234",
    }


@pytest.fixture
def portfolio_data() -> dict:
    mutation = '''
    mutation {
        createOperation(operationData: {
            ticker: "BTCUSDT",
            amount: 3,
            price: 40000,
            type: "buy",
            userId: 0
        }) {
            ticker
            amount
            price
            type
            userId
        }
    }
    '''
    return {"query": mutation}


@pytest.fixture
async def creata_new_user_with_token(not_auth_user_client: AsyncClient):
    user = UserFactory()

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': user.email,
        'password': user.password
    }
    response = await not_auth_user_client.post("api/auth/login", data=data, headers=headers)
    data = response.json()
    print(11111111111111)
    print(data)
    print(user.email)
    print(user.password)
    return data.get('access_token')

