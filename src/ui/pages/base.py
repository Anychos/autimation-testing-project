from httpx import URL
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url: URL) -> Page:
        self.page.goto(url)

    def reload(self) -> Page:
        self.page.reload()
