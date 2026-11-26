from http import HTTPStatus
from typing import Any

import allure

from src.api.schemas.errors import BaseErrorSchema, ErrorDetailSchema, HttpErrorSchema


@allure.step("Проверка статус кода ответа")
def assert_status_code(expected: HTTPStatus, actual: int) -> None:
    assert expected == actual, (
        f"Статус код не соответсвует ожидаемому. Получен {actual}, ожидался {expected}"
    )


@allure.step("Проверка значения в поле {field}")
def assert_field_value(expected: Any, actual: Any, field: str) -> None:
    assert expected == actual, (
        f"Значение в поле {field} не соответсвует ожидаемому. Получено {actual}, ожидалось {expected}"
    )


@allure.step("Проверка содержимого ответа об ошибке")
def assert_http_error_response(
    *,
    actual_response: HttpErrorSchema,
    expected_response: HttpErrorSchema,
) -> None:
    assert_field_value(
        expected=expected_response.error.code,
        actual=actual_response.error.code,
        field="error.code",
    )
    assert_field_value(
        expected=expected_response.error.message,
        actual=actual_response.error.message,
        field="error.message",
    )
    assert_field_value(
        expected=expected_response.error.details,
        actual=actual_response.error.details,
        field="error.details",
    )


@allure.step("Проверка ответа об ошибке валидации")
def assert_validation_error_response(
    *,
    actual_response: HttpErrorSchema,
    expected_details: list[ErrorDetailSchema],
) -> None:
    expected_response = HttpErrorSchema(
        error=BaseErrorSchema(
            code="VALIDATION_ERROR",
            message="Invalid request data",
            details=expected_details,
        )
    )

    assert_http_error_response(
        actual_response=actual_response,
        expected_response=expected_response,
    )
