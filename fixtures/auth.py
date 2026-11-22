from collections.abc import Iterator

import pytest
from pydantic import BaseModel, EmailStr

from clients.auth import AuthAPIClient, get_auth_client
from schemas.auth import (
    LoginRequestSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


class UserFixture(BaseModel):
    request: RegisterRequestSchema
    response: RegisterResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def login_data(self) -> LoginRequestSchema:
        return LoginRequestSchema(
            email=self.request.email, password=self.request.password
        )


@pytest.fixture
def auth_client() -> Iterator[AuthAPIClient]:
    client = get_auth_client()
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def registered_user(auth_client: AuthAPIClient) -> UserFixture:
    register_request = RegisterRequestSchema()
    register_response = auth_client.register(body=register_request)
    return UserFixture(request=register_request, response=register_response)
