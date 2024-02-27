from typing import Sequence

from db.database import get_async_session
from fastapi import Depends, HTTPException, status
from portfolio.models import Portfolio
from portfolio.portfolio_schemas import PortfolioCreateSchema
from sqlalchemy import Row, case, delete, distinct, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class PortfolioRepo:
    """Portfolio Repo"""

    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session)
    ) -> None:
        self.session = session

    async def check_diff_amount(
            self, user_id: int,
            new_operation: PortfolioCreateSchema
    ) -> HTTPException | bool:
        """Check diff amount between ticker with type buy and sell"""
        stmt = (
            select(
                func.coalesce(
                    func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
                    func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0)), 0)
                .label('diff_amount'))
            .where(
                (Portfolio.user_id == user_id) &
                (Portfolio.ticker == new_operation.ticker)
            )
        )
        result = (await self.session.execute(stmt)).scalars().first()
        if result - new_operation.amount < 0 and new_operation.type != 'buy':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You cant to sell more than buy',
            )
        return True

    async def get_unique_user_ticker(self, user_id) -> Sequence[Row]:
        """get unique user ticker by user_id"""
        stmt = select(distinct(Portfolio.ticker)).where(Portfolio.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_operation(
            self,
            user_id: int
    ) -> Sequence[Row]:
        """Get list operations"""
        stmt = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_operation(
            self,
            user_id: int,
            new_operation: PortfolioCreateSchema
    ) -> Sequence[Row]:
        """Create operation"""
        await self.check_diff_amount(user_id=user_id, new_operation=new_operation)

        new_operation.user_id = user_id
        stmt = insert(Portfolio).values(new_operation.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.list_operation(user_id=user_id)

    async def delete_operation(
            self,
            user_id: int,
            operation_id: int
    ) -> Sequence[Row]:
        """Delete operation"""
        stmt = delete(Portfolio).where(Portfolio.id == operation_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.list_operation(user_id=user_id)
