from playwright.sync_api import Locator, Page

from src.ui.components.base import BaseComponent


class BaseForm(BaseComponent):
    def __init__(self, page: Page, form_box: str) -> None:
        super().__init__(page)

        self.form_box = self.page.locator(f"div.{form_box}")
        self.form_title = self.form_box.get_by_role(role="heading")
        self.title_subtext = self.form_box.locator("p.muted")

    def field_label(self, field_name: str) -> Locator:
        return self.form_box.locator(f"label[for='{field_name}']")

    def input(self, test_id: str) -> Locator:
        return self.form_box.get_by_test_id(test_id)

    def button(self, test_id: str) -> Locator:
        return self.form_box.get_by_test_id(test_id)

    def error_message(self, field_name: str) -> Locator:
        return self.form_box.locator(f"span[id='{field_name}-error']")

    def fill_field(self, field_test_id: str, value: str) -> None:
        self.input(field_test_id).fill(value)

    def clear_field(self, field_test_id: str) -> None:
        self.input(field_test_id).clear()

    def click_button(self, button_test_id: str) -> None:
        self.button(button_test_id).click()
