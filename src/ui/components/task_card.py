from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class TaskCard(BaseComponent):
    def __init__(self, page: Page, task_id: str) -> None:
        super().__init__(page)
        self.card = page.get_by_test_id(f"task-card-{task_id}")

        self.status_icon = self.card.locator(".task-status-icon")
        self.details = self.card.locator(".task-details")
        self.title = self.details.locator("h3")
        self.status = self.details.locator(".status-badge")
        self.due_date = self.details.locator(".due-date")

        self.actions = self.card.locator(".task-actions")
        self.edit_button = self.card.get_by_test_id(f"edit-task-{task_id}")
        self.delete_button = self.card.get_by_test_id(f"delete-task-{task_id}")

    def check_visibility(self) -> None:
        expect(self.card).to_be_visible()
        expect(self.status_icon).to_be_visible()
        expect(self.title).to_be_visible()
        expect(self.status).to_be_visible()
        expect(self.due_date).to_be_visible()
        expect(self.edit_button).to_be_visible()
        expect(self.delete_button).to_be_visible()

    def check_title(self, title: str) -> None:
        expect(self.title).to_have_text(title)

    def check_status(self, status: str) -> None:
        expect(self.status).to_have_text(status)

    def check_due_date(self, due_date: str) -> None:
        expect(self.due_date).to_have_text(due_date)

    def click_edit_button(self) -> None:
        self.edit_button.click()

    def click_delete_button(self) -> None:
        self.delete_button.click()
