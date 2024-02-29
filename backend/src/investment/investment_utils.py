from typing import Sequence

from investment.investment_schemas import InvestmentSchema, OperationSumSchema
from sqlalchemy import Row, RowMapping


class InvestmentSchemaConverter:
    """Portfolio schema converter"""
    @staticmethod
    async def convert_list_dict_to_list_schema(
            list_dict: list[dict]
    ) -> list[OperationSumSchema]:
        """convert list sequence row to list PortfolioSchema"""
        return [
            OperationSumSchema.model_validate(obj)
            for obj in list_dict
        ]

    @staticmethod
    async def convert_list_row_to_list_schema(
            list_row: Sequence[RowMapping]
    ) -> list[InvestmentSchema]:
        """convert list sequence row to list PortfolioSchema"""
        return [
            InvestmentSchema.model_validate(investment)
            for investment in list_row
        ]


class InvestmentUtils:
    """Investment Utils"""
    async def prepare_tickers_for_get_price(self, list_tickers: list[dict] | Sequence[Row]):
        """Get list tickers and create string with that list tickers"""
        if len(list_tickers) and isinstance(list_tickers[0], str):
            return (str(list_tickers)).replace(' ', '').replace("'", '"')
        list_tickers = list(map(lambda obj: obj.get('ticker'), list_tickers))
        return (str(list_tickers)).replace(' ', '').replace("'", '"')

    async def update_current_ticker_price(
            self,
            list_difference: Sequence[RowMapping],
            list_dict_prices: list[dict]
    ) -> list[dict]:
        """
        Get from binance api current prices tickers
        Return list with price ticker * amount ticker
        """
        list_updated_ticker_prices = []
        list_sorted_dict_prices: list = sorted(list_dict_prices, key=lambda x: x.get('symbol'))
        for (obj, amount) in zip(list_sorted_dict_prices, list_difference):
            list_updated_ticker_prices.append(
                {
                    'symbol': obj.get('symbol'),
                    'price': float(obj.get('openPrice')) * float(amount.get('amount_difference'))
                }
            )
        return list_updated_ticker_prices
