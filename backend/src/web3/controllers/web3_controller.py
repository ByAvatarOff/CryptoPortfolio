from __future__ import annotations

from typing import TYPE_CHECKING

from src.auth.models import User
from src.web3.domain.services.web3_service import Web3Service
from src.portfolio.schemas.schema import PortfolioCreateSchema


if TYPE_CHECKING:
    from src.web3.schemas.schema import Web3PortfolioCreateSchema
    from src.portfolio.domain.services.portfolio_service import PortfolioService
    from src.portfolio.domain.services.operation_service import OperationService


class Web3Controller:
    def __init__(
            self,
            user: User,
            web3_service: Web3Service,
            portfolio_service: PortfolioService,
            operation_service: OperationService,
    ) -> None:
        self.user = user
        self.web3_service = web3_service
        self.portfolio_service = portfolio_service
        self.operation_service = operation_service

    async def create_web3_portfolio(self, web3_data: Web3PortfolioCreateSchema):
        """TODO create transaction"""
        portfolio = await self.portfolio_service.create(
            new_portfolio=PortfolioCreateSchema(
                name=web3_data.name
            ),
            user_id=self.user.id
        )
        wallet_info = await self.web3_service.get_waller_info(
            web3_data=web3_data,
            portfolio_id=portfolio.id
        )
        await self.operation_service.bulk_create(
            operations=wallet_info,
            user_id=self.user.id
        )
        return portfolio
