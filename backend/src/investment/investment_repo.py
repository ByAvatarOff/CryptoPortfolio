from sqlalchemy import select, case, func, RowMapping
from typing import Sequence
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from portfolio.models import Portfolio


class InvestmentRepo:
    """Investment Repo"""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_difference_type(self, user_id: int) -> Sequence[RowMapping]:
        """Find difference"""
        cte_buy_sell = select(
            Portfolio.ticker,
            (
                func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
                func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0))
            ).label('amount_difference'),
            (
                    func.sum(case((Portfolio.type == 'buy', Portfolio.amount * Portfolio.price), else_=0)) -
                    func.sum(case((Portfolio.type == 'sell', Portfolio.amount * Portfolio.price), else_=0))
            ).label('price_difference'),
        ).where(Portfolio.user_id == user_id).group_by(Portfolio.ticker).cte()

        stmt = select(
            cte_buy_sell.c.ticker,
            cte_buy_sell.c.amount_difference,
            cte_buy_sell.c.price_difference,
            (
                    cte_buy_sell.c.price_difference /
                    func.coalesce(func.NULLIF(cte_buy_sell.c.amount_difference, 0), 1)
            ).label('avg_price'),
        ).select_from(cte_buy_sell).order_by(cte_buy_sell.c.ticker)

        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def get_user_portfolio_price(self, user_id: int) -> RowMapping:
        """Find difference"""
        cte_price_difference = select(
            (
                    func.sum(case((Portfolio.type == 'buy', Portfolio.amount * Portfolio.price), else_=0)) -
                    func.sum(case((Portfolio.type == 'sell', Portfolio.amount * Portfolio.price), else_=0))
            ).label('price_difference')
        ).where(Portfolio.user_id == user_id).group_by(Portfolio.ticker).cte()

        stmt = select(
            func.sum(cte_price_difference.c.price_difference).label('total_price')
        ).select_from(cte_price_difference)

        result = await self.session.execute(stmt)
        return result.mappings().first()
