from __future__ import annotations

from typing import TYPE_CHECKING


from src.core.exceptions import UniquePortfolioError, NotFoundPortfolioError
from src.portfolio.domain.repos.portfolio_repo import PortfolioRepo
from src.portfolio.schemas.schema import PortfolioCreateSchema

if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio


class PortfolioService:
    def __init__(
            self,
            portfolio_repo: PortfolioRepo
    ) -> None:
        self.portfolio_repo = portfolio_repo

    async def create(self, new_portfolio: PortfolioCreateSchema, user_id: int) -> Portfolio:
        if await self.portfolio_repo.get_user_portfolio_by_name(
                portfolio_name=new_portfolio.name,
                user_id=user_id
        ):
            raise UniquePortfolioError
        return await self.portfolio_repo.create(
            new_portfolio=new_portfolio,
            user_id=user_id,
        )

    async def list(self, user_id: int) -> list[Portfolio]:
        return await self.portfolio_repo.list(user_id=user_id)

    async def delete(self, user_id: int, portfolio_id: int) -> None:
        if not await self.portfolio_repo.get_user_portfolio_by_id(portfolio_id=portfolio_id, user_id=user_id):
            raise NotFoundPortfolioError
        await self.portfolio_repo.delete(user_id=user_id, portfolio_id=portfolio_id)
