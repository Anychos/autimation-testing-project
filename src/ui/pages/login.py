from playwright.sync_api import Page

from src.ui.components.auth_form import AuthForm
from src.ui.components.auth_story import AuthStory
from src.ui.pages.base import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.story = AuthStory(page)
        self.form = AuthForm(page)
