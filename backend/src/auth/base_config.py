from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.core.settings import settings


bearer_transport = BearerTransport(tokenUrl='api/auth/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.app.secret_auth, lifetime_seconds=86400)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],

)
current_user = fastapi_users.current_user()
