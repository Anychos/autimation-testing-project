from httpx import Client

from src.api.config import settings


def public_client_builder() -> Client:
    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Origin": settings.http_client.url.rstrip("/")},
    )
