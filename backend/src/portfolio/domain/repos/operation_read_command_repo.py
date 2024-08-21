from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import case, distinct, func, select

from src.portfolio.models.models import Operation, Portfolio
from src.portfolio.schemas.enum import OperationTypeEnum
from src.portfolio.schemas.schema import OperationCreateSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class OperationReadCommandRepo:
    def __init__(
            self,
            session: AsyncSession
    ) -> None:
        self.session = session
        self.model: type[Operation] = Operation

    async def get_operation_by_id(
            self,
            user_id: int,
            operation_id: int
    ) -> Operation:
        stmt = select(self.model).join(Portfolio).where(
            self.model.id == operation_id,
            Portfolio.user_id == user_id
        )
        record = await self.session.execute(stmt)
        return record.scalar()

    async def check_diff_amount(
            self,
            portfolio_id: int,
            new_operation: OperationCreateSchema
    ) -> bool:
        if new_operation.type == OperationTypeEnum.BUY:
            return True
        stmt = (
            select(
                func.coalesce(
                    func.sum(case((self.model.type == OperationTypeEnum.BUY, self.model.amount), else_=0)) -
                    func.sum(case((self.model.type == OperationTypeEnum.SELL, self.model.amount), else_=0)),
                    0)
                .label('diff_amount'))
            .where(
                self.model.portfolio_id == portfolio_id,
                self.model.ticker == new_operation.ticker
            )
        )
        result = (await self.session.execute(stmt)).scalars().first()
        if result - new_operation.amount >= 0:
            return True

    async def get_unique_user_ticker(self, user_id):
        stmt = select(distinct(self.model.ticker)).where(self.model.portfolio.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_difference_type(self, user_id: int) -> list[dict]:
        cte_buy_sell = select(
            self.model.ticker,
            (
                    func.sum(case((self.model.type == OperationTypeEnum.BUY, self.model.amount), else_=0)) -
                    func.sum(case((self.model.type == OperationTypeEnum.SELL, self.model.amount), else_=0))
            ).label('amount_difference'),
            (
                    func.sum(case((self.model.type == OperationTypeEnum.BUY, self.model.amount * self.model.price), else_=0)) -
                    func.sum(case((self.model.type == OperationTypeEnum.SELL, self.model.amount * self.model.price), else_=0))
            ).label('price_difference'),
        ).join(Portfolio).where(Portfolio.user_id == user_id).group_by(self.model.ticker).cte()

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

    async def get_user_portfolio_price(self, user_id: int) -> dict[str, int]:
        cte_price_difference = select(
            (
                    func.sum(case((self.model.type == OperationTypeEnum.BUY, self.model.amount * self.model.price), else_=0)) -
                    func.sum(case((self.model.type == OperationTypeEnum.SELL, self.model.amount * self.model.price), else_=0))
            ).label('price_difference')
        ).where(Portfolio.user_id == user_id).group_by(self.model.ticker).cte()

        stmt = select(
            func.sum(cte_price_difference.c.price_difference).label('total_price')
        ).select_from(cte_price_difference)

        result = await self.session.execute(stmt)
        return result.mappings().first()
