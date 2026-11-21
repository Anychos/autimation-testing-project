from http import HTTPStatus

import pytest

from assertions.auth import (
    assert_login_response,
    assert_register_response,
)
from assertions.base import assert_http_error_response, assert_status_code, assert_validation_error_response
from clients.auth import AuthAPIClient
from fixtures.auth import UserFixture
from schemas.auth import (
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from schemas.errors import BaseErrorSchema, HttpErrorSchema, ErrorDetailSchema


@pytest.mark.api
@pytest.mark.auth
class TestAuth:
    @pytest.mark.smoke
    def test_registration_new_user_returns_201(
        self, auth_client: AuthAPIClient
    ) -> None:
        register_request = RegisterRequestSchema()
        register_response = auth_client.register_api(body=register_request)
        assert_status_code(
            expected=HTTPStatus.CREATED, actual=register_response.status_code
        )
        response_data = RegisterResponseSchema.model_validate_json(
            register_response.content
        )
        assert_register_response(register_request, response_data)

    @pytest.mark.smoke
    def test_login_existing_user_returns_200(
        self, auth_client: AuthAPIClient, registered_user: UserFixture
    ) -> None:
        login_request = RegisterRequestSchema(
            email=registered_user.email, password=registered_user.password
        )
        login_response = auth_client.login_api(body=login_request)
        assert_status_code(expected=HTTPStatus.OK, actual=login_response.status_code)
        response_data = LoginResponseSchema.model_validate_json(login_response.content)
        assert_login_response(login_request, response_data)

    @pytest.mark.parametrize(
        "email, password, expected_details",
        [
            pytest.param(
                "", "Validpass123!",
                [ErrorDetailSchema(loc=["body", "email"], msg="Value error, Invalid email format", type="value_error")],
                id="empty-email",
            ),
            pytest.param(
                "invalid-email", "Validpass123!",
                [ErrorDetailSchema(loc=["body", "email"], msg="Value error, Invalid email format", type="value_error")],
                id="invalid-email",
            ),
            pytest.param(
                "check@example.com", "",
                [ErrorDetailSchema(loc=["body", "password"], msg="String should have at least 8 characters", type="string_too_short")],
                id="empty-password",
            ),
            pytest.param(
                "check@example.com", "a" * 7,
                [ErrorDetailSchema(loc=["body", "password"], msg="String should have at least 8 characters", type="string_too_short")],
                id="password-min-minus-one",
            ),
            pytest.param(
                "check@example.com", "a" * 65,
                [ErrorDetailSchema(loc=["body", "password"], msg="String should have at most 64 characters", type="string_too_long")],
                id="password-max-plus-one",
            ),
        ],
    )
    def test_registration_incorrect_data_returns_422(
        self,
        auth_client: AuthAPIClient,
        email: str,
        password: str,
        expected_details: list[ErrorDetailSchema],
    ) -> None:
        # Arrange
        register_request = RegisterRequestSchema.model_construct(
            email=email,
            password=password,
        )

        # Act
        register_response = auth_client.register_api(body=register_request)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNPROCESSABLE_ENTITY, actual=register_response.status_code
        )
        response_data = HttpErrorSchema.model_validate_json(register_response.content)
        assert_validation_error_response(response_data, expected_details)

    def test_registration_with_existing_email_returns_409(
        self, auth_client: AuthAPIClient, registered_user: UserFixture
    ) -> None:
        expected_error = HttpErrorSchema(
            error=BaseErrorSchema(
                code="EMAIL_EXISTS",
                message="Email is already registered",
                details=[],
            )
        )
        register_request = RegisterRequestSchema(
            email=registered_user.email, password=registered_user.password
        )
        register_response = auth_client.register_api(body=register_request)
        assert_status_code(
            expected=HTTPStatus.CONFLICT, actual=register_response.status_code
        )
        response_data = HttpErrorSchema.model_validate_json(register_response.content)
        assert_http_error_response(response_data, expected_error)

    def test_login_nonexistent_user_returns_401(
        self, auth_client: AuthAPIClient
    ) -> None:
        expected_error = HttpErrorSchema(
            error=BaseErrorSchema(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                details=[],
            )
        )
        login_request = RegisterRequestSchema()
        login_response = auth_client.login_api(body=login_request)
        assert_status_code(
            expected=HTTPStatus.UNAUTHORIZED, actual=login_response.status_code
        )
        response_data = HttpErrorSchema.model_validate_json(login_response.content)
        assert_http_error_response(response_data, expected_error)

    def test_login_existing_user_incorrect_password_returns_401(
        self, auth_client: AuthAPIClient,
        registered_user: UserFixture
    ) -> None:
        expected_error = HttpErrorSchema(
            error=BaseErrorSchema(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                details=[],
            )
        )
        login_request = RegisterRequestSchema(
            email=registered_user.email
        )
        login_response = auth_client.login_api(body=login_request)
        assert_status_code(
            expected=HTTPStatus.UNAUTHORIZED, actual=login_response.status_code
        )
        response_data = HttpErrorSchema.model_validate_json(login_response.content)
        assert_http_error_response(response_data, expected_error)
