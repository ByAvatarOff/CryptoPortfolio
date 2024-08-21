import factory
from pytest_factoryboy import register
from portfolio.models import Portfolio
from auth.models import User
import contextlib
from auth.utils import get_async_session, get_user_db
from core.database import get_async_session
from auth.schema import UserCreate
from auth.manager import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists


# class UserFactory(object):
#     email = 'test@mail.ru'
#     username = "test_username"
#     password = 'test'
#     get_async_session_context = contextlib.asynccontextmanager(get_async_session)
#     get_user_db_context = contextlib.asynccontextmanager(get_user_db)
#     get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
#
#     async def __call__(self, *args, **kwargs):
#         try:
#             async with self.get_async_session_context() as session:
#                 async with self.get_user_db_context(session) as user_db:
#                     async with self.get_user_manager_context(user_db) as user_manager:
#                         user = await user_manager.create(
#                             UserCreate(
#                                 email=self.email, password=self.password, username=self.username
#                             )
#                         )
#                         return user
#         except UserAlreadyExists:
#             return user
@register
class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.Faker('password')
    username = factory.Faker('email')

    get_async_session_context = contextlib.asynccontextmanager(get_async_session)
    get_user_db_context = contextlib.asynccontextmanager(get_user_db)
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

    async def __call__(self, model_class, *args, **kwargs):
        try:
            async with self.get_async_session_context as session:
                async with self.get_user_db_context(session) as user_db:
                    async with self.get_user_manager_context(user_db) as user_manager:
                        user = await user_manager.create(
                            UserCreate(**kwargs)
                        )
                        return user
        except UserAlreadyExists:
            return user