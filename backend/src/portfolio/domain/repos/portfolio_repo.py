from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, insert, select

from src.portfolio.models.models import Portfolio
from src.portfolio.schemas.schema import PortfolioCreateSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PortfolioRepo:
    def __init__(
            self,
            session: AsyncSession
    ) -> None:
        self.session = session
        self.model: type[Portfolio] = Portfolio

    async def get_user_portfolio_by_name(self, user_id: int, portfolio_name: str) -> Portfolio:
        stmt = select(self.model).where(self.model.name == portfolio_name, self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_portfolio_by_id(self, portfolio_id: int, user_id: int) -> Portfolio:
        stmt = select(self.model).where(self.model.id == portfolio_id, self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create(
            self,
            portfolio_name: str,
            image: str,
            user_id: int,
    ) -> Portfolio:
        to_create_data = {
            "name": portfolio_name,
            "user_id": user_id,
            "image": image,
        }
        stmt = insert(self.model).values(to_create_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def list(self, user_id: int) -> list[Portfolio]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(
            self,
            user_id: int,
            portfolio_id: int
    ) -> None:
        stmt = delete(self.model).where(self.model.id == portfolio_id, self.model.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
