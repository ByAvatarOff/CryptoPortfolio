from sqlalchemy import Float, Column, Integer, String, MetaData, Table, TIMESTAMP, ForeignKey
from datetime import datetime
from auth.models import user


metadata = MetaData()


portfolio = Table(
    "portfolio",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
        Column("ticker", String),
    Column("amount", Float),
    Column("price", Float),
    Column("type", String),
    Column("add_date", TIMESTAMP, default=datetime.utcnow),
    Column('user_id', Integer, ForeignKey(user.c.id))
)