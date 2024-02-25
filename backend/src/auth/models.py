from datetime import datetime
from typing import TYPE_CHECKING

from db.database import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.portfolio.models import Portfolio


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Model of view table User
    """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str]
    username: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=True)
    portfolio: Mapped['Portfolio'] = relationship(cascade='all, delete-orphan')
