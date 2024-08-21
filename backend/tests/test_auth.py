from httpx import AsyncClient


class TestAuth:
    register_url = "api/auth/register"
    login_url = "api/auth/login"

    async def test_register(self, not_auth_user_client: AsyncClient, user_data_register: dict):
        response = await not_auth_user_client.post(url=self.register_url, json=user_data_register)
        assert response.status_code == 201

    async def test_login(self, not_auth_user_client: AsyncClient, user_data_login):
        response = await not_auth_user_client.post(self.login_url, data=user_data_login)
        assert response.status_code == 200
        data = response.json()
        assert data.get('token_type') == 'bearer'
        assert data.get('access_token', '') != ''
