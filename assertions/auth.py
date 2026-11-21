from assertions.base import assert_field_value
from schemas.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)


def assert_register_response(
    register_request: RegisterRequestSchema, register_response: RegisterResponseSchema
) -> None:
    assert_field_value(register_request.email, register_response.email, "email")


def assert_login_response(
    login_request: LoginRequestSchema, login_response: LoginResponseSchema
) -> None:
    assert_field_value(login_request.email, login_response.email, "email")
