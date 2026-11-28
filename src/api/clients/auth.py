import allure
from httpx import Response

from src.api.clients.base import BaseAPIClient
from src.api.clients.public_builder import public_client_builder
from src.api.schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from src.api.tools.coverage import coverage_tracker
from src.api.tools.routes import Route


class AuthAPIClient(BaseAPIClient):
    @allure.step("Отправка запроса на регистрацию")
    @coverage_tracker.track_coverage_httpx(Route.REGISTER)
    def register_api(self, *, body: RegisterRequestSchema) -> Response:
        return self.post(url=Route.REGISTER, json=body.model_dump(mode="json"))

    def register(self, *, body: RegisterRequestSchema) -> RegisterResponseSchema:
        response = self.register_api(body=body)
        response.raise_for_status()
        response_data = RegisterResponseSchema.model_validate_json(response.content)
        return response_data

    @allure.step("Отправка запроса на логин")
    @coverage_tracker.track_coverage_httpx(Route.LOGIN)
    def login_api(self, *, body: LoginRequestSchema) -> Response:
        return self.post(url=Route.LOGIN, json=body.model_dump(mode="json"))

    def login(self, *, body: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(body=body)
        response.raise_for_status()
        response_data = LoginResponseSchema.model_validate_json(response.content)
        return response_data

    @allure.step("Отправка запроса на получение данных текущего пользователя")
    @coverage_tracker.track_coverage_httpx(Route.GET_USER_ME)
    def get_user_me_api(self) -> Response:
        return self.get(url=Route.GET_USER_ME)


def get_auth_client() -> AuthAPIClient:
    return AuthAPIClient(client=public_client_builder())
