from httpx import URL
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url: URL) -> Page:
        self.page.goto(url)

    def reload(self) -> Page:
        self.page.reload()

    def check_current_page_url(self, expected_url: str) -> None:
        expect(self.page).to_have_url(expected_url)
