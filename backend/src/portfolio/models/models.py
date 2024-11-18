from datetime import datetime

from src.auth.models import User
from src.core.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Portfolio(Base):
    __tablename__ = 'portfolio'

    name: Mapped[str]
    image: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))
    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="portfolio")

    __table_args__ = (UniqueConstraint('name', 'user_id'),)


class Operation(Base):
    __tablename__ = 'operation'

    ticker: Mapped[str]
    amount: Mapped[float]
    price: Mapped[float]
    type: Mapped[str]
    add_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    portfolio_id: Mapped[int] = mapped_column(ForeignKey(Portfolio.id, ondelete='CASCADE'))
    portfolio: Mapped["Portfolio"] = relationship(Portfolio, back_populates="operations")
