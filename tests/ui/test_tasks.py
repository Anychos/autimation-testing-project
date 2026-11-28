from uuid import UUID

import pytest

from src.api.fixtures.tasks import TaskFixture
from src.ui.pages.tasks_dashboard import TasksDashboardPage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.tasks
class TestTasksUI:
    def test_create_task(
        self, dashboard_page: TasksDashboardPage, task_ids_to_cleanup: list[UUID]
    ) -> None:
        # Arrange
        page = dashboard_page.page
        dashboard_page.open(dashboard_page.URL)
        title = "Prepare release checklist"
        dashboard_page.open_create_task()
        dashboard_page.task_form.fill_form(title, "Release details", "todo")

        # Act
        with page.expect_response(
            lambda response: (
                response.request.method == "POST"
                and response.url.endswith("/api/v1/tasks")
            )
        ) as response_info:
            dashboard_page.task_form.click_save()
        response = response_info.value
        task_id = UUID(response.json()["id"])
        task_ids_to_cleanup.append(task_id)

        # Assert
        assert response.status == 201
        dashboard_page.check_task_visible(str(task_id), title)
        dashboard_page.reload()
        dashboard_page.check_task_visible(str(task_id), title)

    def test_edit_task(
        self, dashboard_page: TasksDashboardPage, created_task: TaskFixture
    ) -> None:
        # Arrange
        dashboard_page.open(dashboard_page.URL)
        task_id = str(created_task.task_id)
        dashboard_page.check_task_visible(task_id, created_task.request.title)

        # Act
        dashboard_page.task_card(task_id).click_edit_button()
        dashboard_page.task_form.fill_form("Updated task", "Updated details", "done")
        dashboard_page.task_form.click_save()
        dashboard_page.task_form.check_closed()
        dashboard_page.reload()

        # Assert
        dashboard_page.check_task_visible(task_id, "Updated task")
        dashboard_page.task_card(task_id).check_status("Completed")

    def test_delete_task(
        self, dashboard_page: TasksDashboardPage, created_task: TaskFixture
    ) -> None:
        # Arrange
        dashboard_page.open(dashboard_page.URL)
        task_id = str(created_task.task_id)
        dashboard_page.check_task_visible(task_id, created_task.request.title)

        # Act
        dashboard_page.task_card(task_id).click_delete_button()
        dashboard_page.confirm_delete_task()
        dashboard_page.task_form.check_closed()
        dashboard_page.reload()

        # Assert
        dashboard_page.check_empty_state()
        dashboard_page.check_task_absent(task_id)
