from collections.abc import Iterator

import pytest

from clients.auth import AuthAPIClient
from clients.tasks import TasksAPIClient, get_tasks_client
from fixtures.auth import UserFixture


@pytest.fixture
def tasks_client(
    auth_client: AuthAPIClient, registered_user: UserFixture
) -> Iterator[TasksAPIClient]:
    client = get_tasks_client(
        auth_client=auth_client, login_data=registered_user.login_data
    )
    try:
        yield client
    finally:
        client.close()
