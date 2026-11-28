from datetime import date
from typing import Literal

from playwright.sync_api import Locator, Page, expect

from src.ui.components.base_form import BaseForm


class CreateTaskForm(BaseForm):
    def __init__(self, page: Page) -> None:
        super().__init__(page, form_box=page.get_by_test_id("task-dialog"))

        self.close_form_button = self.form_box.get_by_role(
            role="button", name="Close dialog"
        )

        self.title_input = self.form_box.get_by_test_id("task-title-input")
        self.description_input = self.form_box.get_by_test_id("task-description-input")
        self.status_input = self.form_box.get_by_test_id("task-status-input")
        self.due_date_input = self.form_box.get_by_test_id("task-due-date-input")

        self.save_button = self.form_box.get_by_test_id("task-save")
        self.cancel_button = self.form_box.get_by_test_id("task-cancel")

    def status_dropdown_option(
        self, status: Literal["todo", "in_progress", "done"]
    ) -> Locator:
        return self.status_input.locator(f"option[value='{status}']")

    def select_due_date(self, due_date: date) -> None:
        self.due_date_input.fill(due_date.isoformat())

    def clear_due_date(self) -> None:
        self.due_date_input.clear()

    def fill_form(
        self,
        title: str,
        description: str | None = None,
        status: Literal["todo", "in_progress", "done"] = "todo",
        due_date: date | None = None,
    ) -> None:
        self.title_input.fill(title)

        if description is not None:
            self.description_input.fill(description)

        self.status_input.select_option(status)

        if due_date is not None:
            self.due_date_input.fill(due_date.isoformat())

    def check_visibility(self) -> None:
        expect(self.form_title).to_be_visible()
        expect(self.form_title).to_have_text("Create task")

        expect(self.title_subtext).to_be_visible()
        expect(self.title_subtext).to_have_text(
            "A clear next step makes all the difference."
        )

        expect(self.close_form_button).to_be_visible()

        expect(self.field_label("title")).to_be_visible()
        expect(self.field_label("title")).to_have_text("Title")

        expect(self.title_input).to_be_visible()

        expect(self.field_label("description")).to_be_visible()
        expect(self.field_label("description")).to_have_text("Description")

        expect(self.description_input).to_be_visible()

        expect(self.field_label("status")).to_be_visible()
        expect(self.field_label("status")).to_have_text("Status")

        expect(self.status_input).to_be_visible()

        expect(self.field_label("due_date")).to_be_visible()
        expect(self.field_label("due_date")).to_have_text("Due date")

        expect(self.due_date_input).to_be_visible()

        expect(self.cancel_button).to_be_visible()
        expect(self.save_button).to_be_visible()

    def check_title_error(self, message: str) -> None:
        self.check_field_error("title", message)

    def check_closed(self) -> None:
        expect(self.form_box).to_be_hidden()

    def clear_title_input(self) -> None:
        self.title_input.clear()

    def clear_description_input(self) -> None:
        self.description_input.clear()

    def clear_due_date_input(self) -> None:
        self.due_date_input.clear()

    def click_close(self) -> None:
        self.close_form_button.click()

    def click_save(self) -> None:
        self.save_button.click()

    def click_cancel(self) -> None:
        self.cancel_button.click()
