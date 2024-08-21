from src.auth.models import User
from src.binance_api.domain.services.http_service import BinanceService


class BinanceController:
    def __init__(
            self,
            user: User,
            binance_service: BinanceService
    ) -> None:
        self.user = user
        self.binance_service = binance_service

    async def list_all_tickers(self) -> list[str]:
        return await self.binance_service.list_all_tickers()

    async def ticker_price_changes(self):
        return await self.binance_service.ticker_price_changes(user_id=self.user.id)