class InvestmentUtils:
    @staticmethod
    def prepare_tickers_for_get_price(list_tickers: list[dict]) -> str:
        if len(list_tickers) and isinstance(list_tickers[0], str):
            return (str(list_tickers)).replace(' ', '').replace("'", '"')
        list_tickers = list(map(lambda obj: obj.get('ticker'), list_tickers))
        return (str(list_tickers)).replace(' ', '').replace("'", '"')

    @staticmethod
    async def update_current_ticker_price(
            list_difference: list[dict],
            list_dict_prices: list[dict]
    ) -> list[dict]:
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
