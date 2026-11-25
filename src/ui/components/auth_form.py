from playwright.sync_api import Page

from src.ui.components.base_form import BaseForm


class AuthForm(BaseForm):
    def __init__(self, page: Page, form_box: str = "auth-box") -> None:
        super().__init__(page, form_box)

        self.welcome_text = self.form_box.locator("span.eyebrow")
        self.switch_form_text = self.form_box.locator("p.auth-switch")
        self.switch_form_link = self.form_box.get_by_test_id("auth-switch")

    def click_link(self) -> None:
        self.switch_form_link.click()
