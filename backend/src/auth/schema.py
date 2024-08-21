from fastapi_users import schemas
from pydantic import ConfigDict


class UserRead(schemas.BaseUser[int]):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
