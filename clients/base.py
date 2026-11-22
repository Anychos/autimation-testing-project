from typing import Any

from httpx import URL, Client, Response


class BaseAPIClient:
    def __init__(self, client: Client) -> None:
        self.client = client

    def close(self) -> None:
        self.client.close()

    def get(
        self,
        *,
        url: URL,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        return self.client.get(url=url, params=params, headers=headers)

    def post(
        self,
        *,
        url: URL,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
    ) -> Response:
        return self.client.post(url=url, headers=headers, json=json)

    def patch(
        self,
        *,
        url: URL,
        headers: dict[str, str] | None = None,
        json: Any | None = None,
    ) -> Response:
        return self.client.patch(url=url, headers=headers, json=json)

    def delete(
        self,
        *,
        url: URL,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        return self.client.delete(url=url, params=params, headers=headers)
