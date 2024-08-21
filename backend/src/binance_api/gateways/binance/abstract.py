from abc import ABC, abstractmethod


class ExternalClient(ABC):
    @abstractmethod
    async def get(self, url: str, params: dict = None) -> dict | list[dict]: ...
