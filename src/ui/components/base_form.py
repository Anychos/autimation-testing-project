from playwright.sync_api import Locator, Page, expect

from src.ui.components.base import BaseComponent


class BaseForm(BaseComponent):
    def __init__(self, page: Page, form_box: Locator) -> None:
        super().__init__(page)
        self.form_box = form_box

        self.form_title = self.form_box.get_by_role(role="heading")
        self.title_subtext = self.form_box.locator("p.muted")

    def error_message(self, field_name: str) -> Locator:
        return self.form_box.locator(f"span[id='{field_name}-error']")

    def check_field_error(self, field_name: str, message: str) -> None:
        expect(self.error_message(field_name)).to_be_visible()
        expect(self.error_message(field_name)).to_contain_text(message)
