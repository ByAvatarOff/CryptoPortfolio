from src.auth.models import User
from src.investment.domain.services.service import InvestmentService
from src.investment.schemas.schema import AllTimeProfitSchema


class InvestmentController:
    def __init__(
            self,
            user: User,
            investment_service: InvestmentService
    ) -> None:
        self.user = user
        self.investment_service = investment_service

    async def list_tickers_stat(self, portfolio_id: int) -> list[dict]:
        return await self.investment_service.list_tickers_stat(
            user_id=self.user.id,
            portfolio_id=portfolio_id,
        )

    async def sum_operations(self) -> list[dict]:
        return await self.investment_service.sum_operations(user_id=self.user.id)

    async def all_time_profit(self, period: str) -> AllTimeProfitSchema:
        return await self.investment_service.all_time_profit(
            user_id=self.user.id,
            period=period
        )