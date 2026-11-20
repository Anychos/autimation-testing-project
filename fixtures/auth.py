from pydantic import BaseModel, EmailStr
import pytest

from clients.auth import AuthAPIClient, get_auth_client
from schemas.auth import RegisterRequestSchema, RegisterResponseSchema


class UserFixture(BaseModel):
    request: RegisterRequestSchema
    response: RegisterResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

@pytest.fixture 
def auth_client() -> AuthAPIClient:
    return get_auth_client()

@pytest.fixture 
def registered_user(auth_client: AuthAPIClient) -> UserFixture:
    register_request = RegisterRequestSchema()
    register_response = auth_client.register(body=register_request)
    return UserFixture(request=register_request, response=register_response)