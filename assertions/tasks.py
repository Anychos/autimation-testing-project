from uuid import UUID

from assertions.base import assert_field_value
from schemas.tasks import (
    BaseTaskSchema,
    CreateTaskRequestSchema,
    CreateTaskResponseSchema,
    GetTaskResponseSchema,
    GetTasksResponseSchema,
    PaginationSchema,
    PatchTaskRequestSchema,
    PatchTaskResponseSchema,
)


def assert_base_task_fields(expected: BaseTaskSchema, actual: BaseTaskSchema) -> None:
    assert_field_value(expected.title, actual.title, "title")
    assert_field_value(expected.description, actual.description, "description")
    assert_field_value(expected.status, actual.status, "status")
    assert_field_value(expected.due_date, actual.due_date, "due_date")
    assert_field_value(expected.id, actual.id, "id")
    assert_field_value(expected.owner_id, actual.owner_id, "owner_id")
    assert_field_value(expected.created_at, actual.created_at, "created_at")
    assert_field_value(expected.updated_at, actual.updated_at, "updated_at")


def assert_create_task_response(
    request: CreateTaskRequestSchema, response: CreateTaskResponseSchema, owner_id: UUID
) -> None:
    assert_field_value(request.title.strip(), response.title, "title")
    assert_field_value(request.description, response.description, "description")
    assert_field_value(request.status, response.status, "status")
    assert_field_value(request.due_date, response.due_date, "due_date")
    assert_field_value(owner_id, response.owner_id, "owner_id")


def assert_get_task_response(
    created_task_response: CreateTaskResponseSchema,
    get_task_response: GetTaskResponseSchema,
) -> None:
    assert_base_task_fields(created_task_response, get_task_response)


def assert_patch_task_response(
    patch_request: PatchTaskRequestSchema,
    task_before_update: BaseTaskSchema,
    patch_response: PatchTaskResponseSchema,
) -> None:
    for field in ("title", "description", "status", "due_date"):
        if field in patch_request.model_fields_set:
            expected_value = getattr(patch_request, field)
            if field == "title" and isinstance(expected_value, str):
                expected_value = expected_value.strip()
        else:
            expected_value = getattr(task_before_update, field)
        assert_field_value(expected_value, getattr(patch_response, field), field)

    assert_field_value(task_before_update.id, patch_response.id, "id")
    assert_field_value(task_before_update.owner_id, patch_response.owner_id, "owner_id")
    assert_field_value(
        task_before_update.created_at, patch_response.created_at, "created_at"
    )
    assert patch_response.updated_at >= task_before_update.updated_at, (
        "updated_at раньше исходного значения"
    )


def assert_get_tasks_response(
    expected_items: list[BaseTaskSchema],
    expected_pagination: PaginationSchema,
    actual: GetTasksResponseSchema,
) -> None:
    assert_field_value(len(expected_items), len(actual.items), "items_count")
    for expected_item, actual_item in zip(expected_items, actual.items):
        assert_base_task_fields(expected_item, actual_item)

    assert_field_value(
        expected_pagination.page, actual.pagination.page, "pagination.page"
    )
    assert_field_value(
        expected_pagination.limit, actual.pagination.limit, "pagination.limit"
    )
    assert_field_value(
        expected_pagination.total, actual.pagination.total, "pagination.total"
    )
    assert_field_value(
        expected_pagination.pages, actual.pagination.pages, "pagination.pages"
    )
