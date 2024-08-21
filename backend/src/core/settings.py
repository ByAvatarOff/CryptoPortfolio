from functools import cache
from pydantic import SecretStr

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    secret_auth: str
    origins: list[str] = ['http://localhost:3000', ]

    app_name: str = "Portfolio app"
    description: str = "Portfolio app"
    binance_ticker_price_url: str = '/api/v3/ticker/price'
    binance_list_ticker_price_url: str = '/api/v3/ticker?symbols='
    binance_ws_ticker_price_url: str = 'wss://stream.binance.com:9443/stream?streams='
    binance_ticker_current_price_timeframe: str = '1m'

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DBSettings(BaseSettings):
    db_host: str
    db_name: str
    db_port: int
    db_user: str
    db_pass: SecretStr
    echo: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def _url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def async_url(self) -> str:
        return self._url()


class DBTestSettings(BaseSettings):
    db_test_host: str
    db_test_name: str
    db_test_port: int
    db_test_user: str
    db_test_pass: SecretStr
    echo: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def _url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_test_user}:{self.db_test_password.get_secret_value()}"
            f"@{self.db_test_host}:{self.db_test_port}/{self.db_test_name}"
        )

    @property
    def async_url(self) -> str:
        return self._url()


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    test_db: DBTestSettings = DBTestSettings()

@cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
