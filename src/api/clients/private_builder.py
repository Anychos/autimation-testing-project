from httpx import Client

from src.api.clients.auth import AuthAPIClient
from src.api.config import settings
from src.api.schemas.auth import LoginRequestSchema
from src.api.tools.routes import Route


def private_client_builder(
    auth_client: AuthAPIClient,
    user_login_data: LoginRequestSchema,
) -> Client:
    login_response = auth_client.login_api(body=user_login_data)
    login_response.raise_for_status()

    client = Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        cookies=login_response.cookies,
        headers={"Origin": settings.http_client.url.rstrip("/")},
    )

    try:
        csrf_response = client.get(Route.GET_CSRF)
        csrf_response.raise_for_status()

        csrf_token = csrf_response.json()["csrf_token"]
        client.headers["X-CSRF-Token"] = csrf_token
    except Exception:
        client.close()
        raise

    return client
