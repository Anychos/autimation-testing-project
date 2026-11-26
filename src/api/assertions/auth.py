import allure

from src.api.assertions.base import assert_field_value
from src.api.schemas.auth import (
    RegisterRequestSchema,
    RegisterResponseSchema,
    UserResponseSchema,
)


@allure.step("Валидация схемы ответа на запрос регистрации пользователя")
def assert_register_response(
    register_request: RegisterRequestSchema, register_response: RegisterResponseSchema
) -> None:
    assert_field_value(register_request.email, register_response.email, "email")


@allure.step("Валидация схемы ответа на запрос логина пользователя")
def assert_user_response(
    expected: UserResponseSchema, actual: UserResponseSchema
) -> None:
    assert_field_value(expected.id, actual.id, "id")
    assert_field_value(expected.email, actual.email, "email")
