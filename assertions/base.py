from http import HTTPStatus


def assert_status_code(expected: HTTPStatus, actual: int) -> None:
    assert expected == actual, f"Статус код не соответсвует ожидаемому. Получен {actual}, ожидался {expected}"