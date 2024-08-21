from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str]
    username: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=True)
    portfolio: Mapped['Portfolio'] = relationship(cascade='all, delete-orphan')
