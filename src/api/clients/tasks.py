from uuid import UUID

from httpx import Response

from src.api.clients.auth import AuthAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_builder import private_client_builder
from src.api.schemas.auth import LoginRequestSchema
from src.api.schemas.tasks import (
    CreateTaskRequestSchema,
    CreateTaskResponseSchema,
    GetTasksQueryParamsSchema,
    PatchTaskRequestSchema,
)
from src.api.tools.routes import Route


class TasksAPIClient(BaseAPIClient):
    def create_task_api(self, body: CreateTaskRequestSchema) -> Response:
        return self.post(url=Route.TASKS, json=body.model_dump(mode="json"))

    def create_task(self, body: CreateTaskRequestSchema) -> CreateTaskResponseSchema:
        response = self.create_task_api(body)
        response.raise_for_status()
        response_data = CreateTaskResponseSchema.model_validate_json(response.content)
        return response_data

    def get_tasks_list_api(
        self, params: GetTasksQueryParamsSchema | None = None
    ) -> Response:
        if params is not None:
            query_params = params.model_dump(mode="json", exclude_none=True)
            return self.get(url=Route.TASKS, params=query_params)
        else:
            return self.get(url=Route.TASKS)

    def get_task_api(self, task_id: UUID) -> Response:
        return self.get(url=f"{Route.TASKS}/{task_id}")

    def patch_task_api(self, task_id: UUID, body: PatchTaskRequestSchema) -> Response:
        return self.patch(
            url=f"{Route.TASKS}/{task_id}",
            json=body.model_dump(mode="json", exclude_unset=True),
        )

    def delete_task_api(self, task_id: UUID) -> Response:
        return self.delete(url=f"{Route.TASKS}/{task_id}")


def get_tasks_client(
    auth_client: AuthAPIClient, login_data: LoginRequestSchema
) -> TasksAPIClient:
    return TasksAPIClient(
        client=private_client_builder(
            auth_client=auth_client, user_login_data=login_data
        )
    )
