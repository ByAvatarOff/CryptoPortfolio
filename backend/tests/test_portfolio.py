from httpx import AsyncClient


class TestCreatePortfolioOperation:
    base_url = '/graphql'

    async def test_create_portfolio_operation_success(
            self,
            auth_user_client: AsyncClient,
            portfolio_data: str
    ) -> None:
        response = await auth_user_client.post(url=self.base_url, json=portfolio_data)
        data = response.json()
        print(data)
        assert response.status_code == 201
        assert isinstance(data, list)
        assert len(data) == 1