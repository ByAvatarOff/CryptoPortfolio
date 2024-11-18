from __future__ import annotations

from typing import TYPE_CHECKING

from src.auth.models import User
from src.portfolio.domain.services.portfolio_service import PortfolioService



if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio
    from fastapi import UploadFile


class PortfolioController:
    def __init__(
            self,
            user: User,
            portfolio_service: PortfolioService
    ) -> None:
        self.user = user
        self.portfolio_service = portfolio_service

    async def create(self, name: str, image: UploadFile) -> Portfolio:
        return await self.portfolio_service.create(
            portfolio_name=name,
            image=image,
            user_id=self.user.id
        )

    async def list(self) -> list[Portfolio]:
        return await self.portfolio_service.list(
            user_id=self.user.id
        )

    async def delete(self, portfolio_id: int) -> None:
        await self.portfolio_service.delete(
            user_id=self.user.id,
            portfolio_id=portfolio_id
        )
