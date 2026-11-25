from datetime import date
from typing import Literal

from playwright.sync_api import Locator, Page

from src.ui.components.base_form import BaseForm


class CreateTaskForm(BaseForm):
    def __init__(self, page: Page, form_box: str = "task-dialog"):
        super().__init__(page, form_box)

        self.close_form_button = self.form_box.get_by_role(role="button", name="×")

    def status_dropdown_option(
        self, status: Literal["todo", "in_progress", "done"]
    ) -> Locator:
        return self.input("task-status-input").locator(f"option[value='{status}']")

    def select_due_date(self, due_date: date) -> None:
        self.input("task-due-date-input").fill(due_date.isoformat())

    def clear_due_date(self) -> None:
        self.input("task-due-date-input").clear()
