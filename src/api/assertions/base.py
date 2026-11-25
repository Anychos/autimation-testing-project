from http import HTTPStatus
from typing import Any

from src.api.schemas.errors import BaseErrorSchema, ErrorDetailSchema, HttpErrorSchema


def assert_status_code(expected: HTTPStatus, actual: int) -> None:
    assert expected == actual, (
        f"Статус код не соответсвует ожидаемому. Получен {actual}, ожидался {expected}"
    )


def assert_field_value(expected: Any, actual: Any, field: str) -> None:
    assert expected == actual, (
        f"Значение в поле {field} не соответсвует ожидаемому. Получено {actual}, ожидалось {expected}"
    )


def assert_http_error_response(
    actual_response: HttpErrorSchema,
    expected_response: HttpErrorSchema,
) -> None:
    assert_field_value(
        expected=expected_response.error.code,
        actual=actual_response.error.code,
        field="code",
    )
    assert_field_value(
        expected=expected_response.error.message,
        actual=actual_response.error.message,
        field="message",
    )
    assert_field_value(
        expected=expected_response.error.details,
        actual=actual_response.error.details,
        field="details",
    )


def assert_validation_error_response(
    actual_response: HttpErrorSchema,
    expected_details: list[ErrorDetailSchema],
) -> None:
    expected_error = HttpErrorSchema(
        error=BaseErrorSchema(
            code="VALIDATION_ERROR",
            message="Invalid request data",
            details=expected_details,
        )
    )

    assert_field_value(
        expected=expected_error.error.code,
        actual=actual_response.error.code,
        field="code",
    )
    assert_field_value(
        expected=expected_error.error.message,
        actual=actual_response.error.message,
        field="message",
    )
    assert_field_value(
        expected=expected_error.error.details,
        actual=actual_response.error.details,
        field="details",
    )
