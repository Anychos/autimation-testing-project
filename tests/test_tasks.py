from datetime import date
from http import HTTPStatus
from uuid import UUID

import pytest

from assertions.base import (
    assert_http_error_response,
    assert_status_code,
    assert_validation_error_response,
)
from assertions.tasks import (
    assert_create_task_response,
    assert_get_task_response,
    assert_get_tasks_response,
    assert_patch_task_response,
)
from clients.tasks import TasksAPIClient
from fixtures.auth import UserFixture
from fixtures.tasks import TaskFixture
from schemas.errors import BaseErrorSchema, ErrorDetailSchema, HttpErrorSchema
from schemas.tasks import (
    CreateTaskRequestSchema,
    CreateTaskResponseSchema,
    GetTaskResponseSchema,
    GetTasksQueryParamsSchema,
    GetTasksResponseSchema,
    PaginationSchema,
    PatchTaskRequestSchema,
    PatchTaskResponseSchema,
)


@pytest.mark.api
@pytest.mark.tasks
@pytest.mark.regression
class TestTasks:
    @pytest.mark.smoke
    def test_create_task_returns_201(
        self,
        tasks_client: TasksAPIClient,
        registered_user: UserFixture,
        task_ids_to_cleanup: list[UUID],
    ) -> None:
        # Arrange
        body = CreateTaskRequestSchema(
            description="Review the test results",
            status="in_progress",
            due_date=date(2030, 6, 20),
        )

        # Act
        response = tasks_client.create_task_api(body=body)

        # Assert
        assert_status_code(expected=HTTPStatus.CREATED, actual=response.status_code)
        task = CreateTaskResponseSchema.model_validate_json(response.content)
        task_ids_to_cleanup.append(task.id)
        assert_create_task_response(body, task, registered_user.user_id)

    @pytest.mark.smoke
    def test_get_task_returns_created_task(
        self,
        tasks_client: TasksAPIClient,
        created_task: TaskFixture,
    ) -> None:
        # Act
        response = tasks_client.get_task_api(task_id=created_task.task_id)

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=response.status_code)
        task = GetTaskResponseSchema.model_validate_json(response.content)
        assert_get_task_response(created_task.response, task)

    @pytest.mark.smoke
    def test_get_tasks_returns_created_task(
        self,
        tasks_client: TasksAPIClient,
        created_task: TaskFixture,
    ) -> None:
        # Arrange
        pagination = PaginationSchema(page=1, limit=10, total=1, pages=1)

        # Act
        response = tasks_client.get_tasks_list_api()

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=response.status_code)
        tasks = GetTasksResponseSchema.model_validate_json(response.content)
        assert_get_tasks_response([created_task.response], pagination, tasks)

    @pytest.mark.smoke
    def test_patch_task_returns_updated_task(
        self,
        tasks_client: TasksAPIClient,
        created_task: TaskFixture,
        registered_user: UserFixture,
    ) -> None:
        # Arrange
        assert_create_task_response(
            created_task.request, created_task.response, registered_user.user_id
        )
        body = PatchTaskRequestSchema(
            title="Release checklist completed", status="done"
        )

        # Act
        response = tasks_client.patch_task_api(task_id=created_task.task_id, body=body)

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=response.status_code)
        task = PatchTaskResponseSchema.model_validate_json(response.content)
        assert_patch_task_response(body, created_task.response, task)
        saved_response = tasks_client.get_task_api(task_id=created_task.task_id)
        assert_status_code(expected=HTTPStatus.OK, actual=saved_response.status_code)
        saved_task = GetTaskResponseSchema.model_validate_json(saved_response.content)
        assert_patch_task_response(body, created_task.response, saved_task)

    @pytest.mark.smoke
    def test_delete_task_returns_204(
        self,
        tasks_client: TasksAPIClient,
        created_task: TaskFixture,
    ) -> None:
        # Act
        response = tasks_client.delete_task_api(task_id=created_task.task_id)

        # Assert
        assert_status_code(expected=HTTPStatus.NO_CONTENT, actual=response.status_code)
        get_response = tasks_client.get_task_api(task_id=created_task.task_id)
        assert_status_code(
            expected=HTTPStatus.NOT_FOUND, actual=get_response.status_code
        )

    @pytest.mark.parametrize("title", ["a" * 3, "a" * 100], ids=["min", "max"])
    def test_create_task_title_boundaries(
        self,
        tasks_client: TasksAPIClient,
        registered_user: UserFixture,
        task_ids_to_cleanup: list[UUID],
        title: str,
    ) -> None:
        # Arrange
        body = CreateTaskRequestSchema(title=title)

        # Act
        response = tasks_client.create_task_api(body=body)

        # Assert
        assert_status_code(expected=HTTPStatus.CREATED, actual=response.status_code)
        task = CreateTaskResponseSchema.model_validate_json(response.content)
        task_ids_to_cleanup.append(task.id)
        assert_create_task_response(body, task, registered_user.user_id)

    @pytest.mark.parametrize(
        "title, message, error_type",
        [
            pytest.param(
                "ab",
                "String should have at least 3 characters",
                "string_too_short",
                id="below-min",
            ),
            pytest.param(
                "a" * 101,
                "String should have at most 100 characters",
                "string_too_long",
                id="above-max",
            ),
        ],
    )
    def test_create_task_invalid_title_returns_422(
        self, tasks_client: TasksAPIClient, title: str, message: str, error_type: str
    ) -> None:
        # Arrange
        body = CreateTaskRequestSchema.model_construct(title=title)
        details = [
            ErrorDetailSchema(loc=["body", "title"], msg=message, type=error_type)
        ]

        # Act
        response = tasks_client.create_task_api(body=body)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNPROCESSABLE_ENTITY, actual=response.status_code
        )
        error = HttpErrorSchema.model_validate_json(response.content)
        assert_validation_error_response(error, details)

    @pytest.mark.parametrize("limit", [0, 51], ids=["below-min", "above-max"])
    def test_get_tasks_invalid_limit_returns_422(
        self, tasks_client: TasksAPIClient, limit: int
    ) -> None:
        # Arrange
        params = GetTasksQueryParamsSchema.model_construct(limit=limit)

        # Act
        response = tasks_client.get_tasks_list_api(params=params)

        # Assert
        assert_status_code(
            expected=HTTPStatus.UNPROCESSABLE_ENTITY, actual=response.status_code
        )
        error = HttpErrorSchema.model_validate_json(response.content)
        assert error.error.code == "VALIDATION_ERROR"
        assert error.error.message == "Invalid request data"
        assert error.error.details[0].loc == ["query", "limit"]

    def test_other_user_cannot_list_read_or_delete_task(
        self,
        tasks_client: TasksAPIClient,
        created_task: TaskFixture,
        second_user_tasks_client: TasksAPIClient,
    ) -> None:
        # Arrange
        task_id = created_task.task_id
        expected_error = HttpErrorSchema(
            error=BaseErrorSchema(
                code="TASK_NOT_FOUND", message="Task not found", details=[]
            )
        )

        # Act
        list_response = second_user_tasks_client.get_tasks_list_api()
        get_response = second_user_tasks_client.get_task_api(task_id=task_id)
        delete_response = second_user_tasks_client.delete_task_api(task_id=task_id)
        owner_response = tasks_client.get_task_api(task_id=task_id)

        # Assert
        assert_status_code(expected=HTTPStatus.OK, actual=list_response.status_code)
        task_list = GetTasksResponseSchema.model_validate_json(list_response.content)
        assert task_list.items == []

        assert_status_code(
            expected=HTTPStatus.NOT_FOUND, actual=get_response.status_code
        )
        get_error = HttpErrorSchema.model_validate_json(get_response.content)
        assert_http_error_response(get_error, expected_error)

        assert_status_code(
            expected=HTTPStatus.NOT_FOUND, actual=delete_response.status_code
        )
        delete_error = HttpErrorSchema.model_validate_json(delete_response.content)
        assert_http_error_response(delete_error, expected_error)

        assert_status_code(expected=HTTPStatus.OK, actual=owner_response.status_code)
        owner_task = GetTaskResponseSchema.model_validate_json(owner_response.content)
        assert_get_task_response(created_task.response, owner_task)
