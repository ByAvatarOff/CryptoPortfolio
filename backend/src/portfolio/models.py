from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db.database import Base
from auth.models import User


class Portfolio(Base):
    """
    Model of view table portfolio
    """
    __tablename__ = 'portfolio'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str]
    amount: Mapped[float]
    price: Mapped[float]
    type: Mapped[str]
    add_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))