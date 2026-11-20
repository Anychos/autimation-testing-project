from httpx import Client

from clients.auth import AuthAPIClient
from schemas.auth import LoginRequestSchema


def private_client_builder(
    auth_client: AuthAPIClient,
    user_login_data: LoginRequestSchema,
) -> Client:
    login_response = auth_client.login_api(body=user_login_data)
    login_response.raise_for_status()

    client = Client(
        base_url="http://localhost:8000/api/v1",
        timeout=50,
        cookies=login_response.cookies,
        headers={"Origin": "http://localhost:8000"}
    )

    csrf_response = client.get("/api/v1/auth/csrf")
    csrf_response.raise_for_status()

    csrf_token = csrf_response.json()["csrf_token"]
    client.headers["X-CSRF-Token"] = csrf_token

    return client