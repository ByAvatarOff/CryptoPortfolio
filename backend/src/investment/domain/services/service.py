from src.binance_api.gateways.binance.binance_http import BinanceAPI
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.investment.schemas.schema import (
    AllTimeProfitSchema,
)
from src.investment.helpers import InvestmentUtils


class InvestmentService:
    def __init__(
            self,
            operation_read_command_repo: OperationReadCommandRepo,
            binance_api: BinanceAPI,
    ):
        self.operation_read_command_repo = operation_read_command_repo
        self.binance_api = binance_api

    async def list_tickers_stat(self, user_id: int, portfolio_id: int) -> list[dict]:
        return await self.operation_read_command_repo.get_difference_type(user_id=user_id, portfolio_id=portfolio_id)

    async def sum_operations(
            self,
            user_id: int
    ) -> list[dict]:
        if not (list_difference := await self.operation_read_command_repo.get_difference_type(user_id=user_id)):
            return []
        list_tickers = InvestmentUtils.prepare_tickers_for_get_price(list_tickers=list_difference)
        list_ticker_current_price = await self.binance_api.get_ticker_current_price(list_tickers=list_tickers)
        result_ticker_prices = await InvestmentUtils.update_current_ticker_price(
            list_difference=list_difference,
            list_dict_prices=list_ticker_current_price
        )
        return result_ticker_prices

    async def all_time_profit(
            self,
            user_id: int,
            period: str
    ) -> AllTimeProfitSchema:
        if not (list_difference := await self.operation_read_command_repo.get_difference_type(user_id=user_id)):
            return AllTimeProfitSchema(profit=0)

        list_tickers = InvestmentUtils.prepare_tickers_for_get_price(list_tickers=list_difference)
        list_ticker_current_price = await self.binance_api.get_ticker_current_price(
            list_tickers=list_tickers,
            period=period,
        )
        binance_actives_price = await InvestmentUtils.update_current_ticker_price(
            list_difference=list_difference,
            list_dict_prices=list_ticker_current_price
        )
        user_actives_total_price = (
            await self.operation_read_command_repo.get_user_portfolio_price(user_id=user_id)
        ).get('total_price', 0)
        return AllTimeProfitSchema.model_validate(
            {
                'profit': sum(map(lambda x: x.get('price', 0), binance_actives_price)) - user_actives_total_price
            }
        )
