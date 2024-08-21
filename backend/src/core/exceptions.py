from fastapi import HTTPException, status


class UniquePortfolioError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Portfolio with taken name is already exists",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class NotFoundPortfolioError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Portfolio not found",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class NotFoundOperationError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Operation not found",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)


class NotEnoughTokenOperationError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "You cant to sell more than to buy",
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
