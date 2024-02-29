from decimal import Decimal


class BinanceTransformer:
    """Binance Transformer"""
    async def transform_responce_to_profit_persent(self, binance_response: list[dict]) -> list[dict]:
        """
        Transform timeframe tickers price to change percent between openPrice and lastPrice
        Return list format {'1d': [{'ticker': 'BTCUSDT', 'percent': '4.18%'},
                                   {'ticker': 'ETHUSDT', 'percent': '3.92%'}]
        """
        format_list = []
        for obj in binance_response:
            percent_change_price = (
                    (Decimal(obj.get('lastPrice')) - Decimal(obj.get('openPrice'))) /
                    Decimal(obj.get('openPrice')) *
                    100
            )
            format_list.append(
                {
                    "ticker": obj.get('symbol'),
                    "percent": f"{percent_change_price:.2f}%"
                }
            )
        return format_list
