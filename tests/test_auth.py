from http import HTTPStatus
from assertions.base import assert_status_code
from clients.auth import AuthAPIClient
from fixtures.auth import UserFixture
from schemas.auth import RegisterRequestSchema


def test_registration_new_user_returns_201(auth_client: AuthAPIClient) -> None:
    register_request = RegisterRequestSchema()
    register_response = auth_client.register_api(body=register_request)
    assert_status_code(expected=HTTPStatus.CREATED, actual=register_response.status_code)

def test_login_existing_user_returns_200(auth_client: AuthAPIClient, registered_user: UserFixture) -> None:
    login_request = RegisterRequestSchema(
        email=registered_user.email,
        password=registered_user.password
    )
    login_response = auth_client.login_api(body=login_request)
    assert_status_code(expected=HTTPStatus.OK, actual=login_response.status_code)


