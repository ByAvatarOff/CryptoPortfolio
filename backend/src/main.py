from auth.base_config import auth_backend, fastapi_users
from auth.schema import UserCreate, UserRead
from binance_api.binance_routers import binance_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from investment.investment_routers import investment_router
from portfolio.portfolio_routers import portfolio_router

app = FastAPI(
    title='Trading App',
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


app.include_router(portfolio_router)
app.include_router(binance_router)
app.include_router(investment_router)


origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
