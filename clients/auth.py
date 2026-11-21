from httpx import URL, Response

from clients.base import BaseAPIClient
from clients.public_builder import public_client_builder
from schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


class AuthAPIClient(BaseAPIClient):
    def register_api(self, *, body: RegisterRequestSchema) -> Response:
        return self.post(url="/auth/register", json=body.model_dump(mode="json"))

    def register(self, *, body: RegisterRequestSchema) -> RegisterResponseSchema:
        response = self.register_api(body=body)
        response.raise_for_status()
        response_data = RegisterResponseSchema.model_validate_json(response.content)
        return response_data

    def login_api(self, *, body: LoginRequestSchema) -> Response:
        return self.post(url="/auth/login", json=body.model_dump(mode="json"))

    def login(self, *, url: URL, body: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(body=body)
        response.raise_for_status()
        response_data = LoginResponseSchema.model_validate_json(response.content)
        return response_data


def get_auth_client() -> AuthAPIClient:
    return AuthAPIClient(client=public_client_builder())
