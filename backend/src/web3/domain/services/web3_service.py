from __future__ import annotations

from typing import TYPE_CHECKING

from src.web3.schemas.schema import Web3PortfolioCreateSchema, Web3Addresses
from src.portfolio.schemas.schema import OperationCreateSchema
from src.portfolio.schemas.enum import OperationTypeEnum
from src.binance_api.gateways.binance.binance_http import BinanceAPI
from src.core.services.thread_pool import ThreadPool
from src.core.services.async_task_pool import AsyncTaskPool
from src.core.settings import settings


if TYPE_CHECKING:
    from src.web3.gateways.moralis.moralis import MoralisClient

class Web3Service:
    def __init__(
            self,
            moralis_client: MoralisClient,
            thread_pool: ThreadPool,
            async_task_pool: AsyncTaskPool,
            binance_api: BinanceAPI
    ) -> None:
        pass
        self.moralis_client = moralis_client
        self.thread_pool = thread_pool
        self.async_task_pool = async_task_pool
        self.binance_api = binance_api

    def _process_wallet_active(self, data: Web3Addresses, portfolio_id: int) -> list[OperationCreateSchema]:
        wallet_token_prices = self.moralis_client.get_wallet_token_prices(
            params={
                "chain": data.blockchain,
                "address": data.address
            }
        )
        return [
            OperationCreateSchema(
                ticker=value.get("symbol"),
                amount=value.get("balance_formatted"),
                price=value.get("usd_price"),
                type=OperationTypeEnum.BUY,
                portfolio_id=portfolio_id,
            )
            for value in wallet_token_prices
            if not value.get("possible_spam") and value.get("usd_price")
        ]

    async def _check_ticker_exists(self, data: OperationCreateSchema) -> OperationCreateSchema:
        ticker = data.ticker + settings.app.app_currency
        ticker_info = await self.binance_api.get_ticker_info(
            ticker=ticker
        )
        if ticker_info.get("symbol"):
            return data

    async def get_waller_info(
            self,
            web3_data: Web3PortfolioCreateSchema,
            portfolio_id: int
    ) -> list[OperationCreateSchema]:
        wallet_tickers, _ = self.thread_pool.run_tasks(
            self._process_wallet_active,
            web3_data.data,
            portfolio_id=portfolio_id
        )
        results, _ = await self.async_task_pool.run_tasks(self._check_ticker_exists, wallet_tickers)
        return results