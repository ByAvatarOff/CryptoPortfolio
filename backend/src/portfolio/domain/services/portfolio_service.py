from __future__ import annotations

import aiofiles
import os
from typing import TYPE_CHECKING

from src.core.settings import settings
from src.core.exceptions import UniquePortfolioError, NotFoundPortfolioError
from src.portfolio.domain.repos.portfolio_repo import PortfolioRepo

if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio
    from fastapi import UploadFile


class PortfolioService:
    def __init__(
            self,
            portfolio_repo: PortfolioRepo
    ) -> None:
        self.portfolio_repo = portfolio_repo

    async def _write_image(
            self,
            image: UploadFile,
            user_id: int,
            portfolio_name: str
    ) -> str:
        full_path = os.path.join(settings.app.upload_image_dir, str(user_id))
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        file_path = f"{user_id}/{portfolio_name}.{image.filename.split('.')[1]}"
        async with aiofiles.open(os.path.join(settings.app.upload_image_dir, file_path), "wb") as file:
            await file.write(await image.read())
        return file_path

    async def create(self, portfolio_name: str, image: UploadFile, user_id: int) -> Portfolio:
        if await self.portfolio_repo.get_user_portfolio_by_name(
                portfolio_name=portfolio_name,
                user_id=user_id
        ):
            raise UniquePortfolioError
        file_path = await self._write_image(image=image, user_id=user_id, portfolio_name=portfolio_name)
        return await self.portfolio_repo.create(
            portfolio_name=portfolio_name,
            user_id=user_id,
            image=file_path,
        )

    async def list(self, user_id: int) -> list[Portfolio]:
        return await self.portfolio_repo.list(user_id=user_id)

    async def delete(self, user_id: int, portfolio_id: int) -> None:
        if not await self.portfolio_repo.get_user_portfolio_by_id(portfolio_id=portfolio_id, user_id=user_id):
            raise NotFoundPortfolioError
        await self.portfolio_repo.delete(user_id=user_id, portfolio_id=portfolio_id)
