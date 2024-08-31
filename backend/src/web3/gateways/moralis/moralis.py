from moralis import evm_api
from openapi_evm_api import ApiException

from src.core.settings import settings


class MoralisClient:
    def __init__(self, api_key: str = settings.app.moralis_api_key):
        self.api_key = api_key

    def get_wallet_token_prices(self, params: dict) -> list[dict]:
        try:
            response = evm_api.wallets.get_wallet_token_balances_price(
                api_key= self.api_key,
                params=params,
            )
            return response.get("result")
        except ApiException:
            return []