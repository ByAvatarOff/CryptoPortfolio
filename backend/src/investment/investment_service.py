from binance_api.binance_utils import BinanceAPI
from fastapi import Depends
from investment.investment_repo import InvestmentRepo
from investment.investment_schemas import (
    AllTimeProfitSchema,
    InvestmentSchema,
    OperationSumSchema,
)
from investment.investment_utils import InvestmentSchemaConverter, InvestmentUtils


class InvestmentService:
    """Portfolio Service"""

    def __init__(
            self,
            investment_repo: InvestmentRepo = Depends(),
            binance_api_service: BinanceAPI = Depends(),
            investment_utils: InvestmentUtils = Depends(),
            investment_converter: InvestmentSchemaConverter = Depends(),
    ):
        self.investment_repo = investment_repo
        self.binance_api_service = binance_api_service
        self.investment_utils = investment_utils
        self.investment_converter = investment_converter

    async def list_investments(
            self,
            user_id: int
    ) -> list[InvestmentSchema]:
        """Get list operations"""
        list_investment = await self.investment_repo.get_difference_type(user_id=user_id)
        return await self.investment_converter.convert_list_row_to_list_schema(
            list_row=list_investment
        )

    async def sum_operations(
            self,
            user_id: int
    ) -> list[OperationSumSchema]:
        """
        Form list with amount tickers with buy and sell
        After request to binance with unique tickers, and it returns price there tickers
        And return result list[dict] with price * amount
        """
        list_difference = await self.investment_repo.get_difference_type(user_id=user_id)
        if not list_difference:
            return []

        list_tickers = await self.investment_utils.prepare_tickers_for_get_price(list_tickers=list_difference)
        list_ticker_current_price = await self.binance_api_service.get_ticker_current_price(list_tickers=list_tickers)
        result_ticker_prices = await self.investment_utils.update_current_ticker_price(
            list_difference=list_difference,
            list_dict_prices=list_ticker_current_price
        )
        return await self.investment_converter.convert_list_dict_to_list_schema(
            list_dict=result_ticker_prices
        )

    async def all_time_profit(
            self,
            user_id: int,
            period: str
    ) -> AllTimeProfitSchema:
        """
        Form list with amount tickers with buy and sell
        After request to binance with unique tickers, and it returns price there tickers
        And return result list[dict] with price * amount
        """
        list_difference = await self.investment_repo.get_difference_type(user_id=user_id)
        if not list_difference:
            return AllTimeProfitSchema.model_validate({'profit': 0})
        list_tickers = await self.investment_utils.prepare_tickers_for_get_price(list_tickers=list_difference)

        list_ticker_current_price = await self.binance_api_service.get_ticker_current_price(
            list_tickers=list_tickers,
            period=period,
        )

        binance_actives_price = await self.investment_utils.update_current_ticker_price(
            list_difference=list_difference,
            list_dict_prices=list_ticker_current_price
        )
        user_actives_total_price = (
            await self.investment_repo.get_user_portfolio_price(user_id=user_id)
        ).get('total_price', 0)
        return AllTimeProfitSchema.model_validate(
            {
                'profit': sum(map(lambda x: x.get('price', 0), binance_actives_price)) - user_actives_total_price
            }
        )
