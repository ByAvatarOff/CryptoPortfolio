from src.binance_api.gateways.binance.binance_http import BinanceAPI
from src.binance_api.schemas.schema import TimeFramePercentChanges
from src.binance_api.helpers import BinanceTransformer
from src.investment.helpers import InvestmentUtils
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.binance_api.schemas.enum import TimeframeChangesEnum


class BinanceService:

    def __init__(
            self,
            binance_api: BinanceAPI,
            operation_read_command_repo: OperationReadCommandRepo,
    ):
        self.binance_api = binance_api
        self.operation_read_command_repo = operation_read_command_repo

    async def list_all_tickers(self) -> list[str]:
        return await self.binance_api.get_list_tickers()

    async def ticker_price_changes(
            self,
            user_id: int,
            portfolio_id: int,
    ) -> TimeFramePercentChanges | None:
        ticker_percent_changes = {}

        if not (unique_user_tickets := await self.operation_read_command_repo.get_unique_user_ticker(
                user_id=user_id,
                portfolio_id=portfolio_id,
        )):
            return TimeFramePercentChanges
        list_tickers = InvestmentUtils.prepare_tickers_for_get_price(list_tickers=unique_user_tickets)

        for timeframe in TimeframeChangesEnum:
            price_change = BinanceTransformer.transform_responce_to_profit_persent(
                await self.binance_api.get_ticker_current_price(
                    list_tickers=list_tickers,
                    period=timeframe
                ))
            ticker_percent_changes.update({
                    f"timeframe_{timeframe}": price_change
                }
            )
        return TimeFramePercentChanges(data=ticker_percent_changes)
