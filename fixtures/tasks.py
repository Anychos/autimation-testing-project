from collections.abc import Iterator
from datetime import date
from http import HTTPStatus
from uuid import UUID

import pytest
from pydantic import BaseModel

from assertions.base import assert_field_value, assert_status_code
from clients.auth import AuthAPIClient
from clients.tasks import TasksAPIClient, get_tasks_client
from fixtures.auth import UserFixture
from schemas.auth import LoginRequestSchema, RegisterRequestSchema
from schemas.errors import HttpErrorSchema
from schemas.tasks import CreateTaskRequestSchema, CreateTaskResponseSchema


class TaskFixture(BaseModel):
    request: CreateTaskRequestSchema
    response: CreateTaskResponseSchema

    @property
    def task_id(self) -> UUID:
        return self.response.id


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


@pytest.fixture
def second_user_tasks_client(auth_client: AuthAPIClient) -> Iterator[TasksAPIClient]:
    registration = RegisterRequestSchema()
    auth_client.register(body=registration)
    login_data = LoginRequestSchema(
        email=registration.email, password=registration.password
    )
    client = get_tasks_client(auth_client=auth_client, login_data=login_data)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def task_ids_to_cleanup(tasks_client: TasksAPIClient) -> Iterator[list[UUID]]:
    task_ids: list[UUID] = []
    yield task_ids

    for task_id in task_ids:
        response = tasks_client.delete_task_api(task_id=task_id)
        if response.status_code == HTTPStatus.NOT_FOUND:
            error = HttpErrorSchema.model_validate_json(response.content)
            assert_field_value("TASK_NOT_FOUND", error.error.code, "error.code")
        else:
            assert_status_code(HTTPStatus.NO_CONTENT, response.status_code)


@pytest.fixture
def created_task(
    tasks_client: TasksAPIClient, task_ids_to_cleanup: list[UUID]
) -> TaskFixture:
    request = CreateTaskRequestSchema(
        description="Prepare the release checklist",
        status="in_progress",
        due_date=date(2030, 6, 15),
    )
    response = tasks_client.create_task(request)
    task_ids_to_cleanup.append(response.id)
    return TaskFixture(request=request, response=response)
