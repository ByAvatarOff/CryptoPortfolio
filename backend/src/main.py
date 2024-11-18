from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.core.settings import settings
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schema import UserCreate, UserRead
from src.binance_api.routes.route import binance_router
from src.investment.routes.route import investment_router
from src.portfolio.routes.operation_route import operation_router
from src.portfolio.routes.portfolio_route import portfolio_router
from src.web3.routes.route import web3_router


app = FastAPI(
    title=settings.app.app_name,
    description=settings.app.description,
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/api/auth',
    tags=['Auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/api/auth',
    tags=['Auth'],
)


app.include_router(binance_router)
app.include_router(investment_router)
app.include_router(operation_router)
app.include_router(portfolio_router)
app.include_router(web3_router)


origins = settings.app.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount("/uploads", StaticFiles(directory=settings.app.upload_image_dir), name="uploads")
