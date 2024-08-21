from decimal import Decimal


class BinanceTransformer:
    @staticmethod
    def transform_responce_to_profit_persent(binance_response: list[dict]) -> list[dict]:
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
