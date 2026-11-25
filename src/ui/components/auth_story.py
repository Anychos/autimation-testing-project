from playwright.sync_api import Page

from src.ui.components.base import BaseComponent


class AuthStory(BaseComponent):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.story_box = self.page.locator("section.auth-story")

        self.brand = self.story_box.locator("span.brand")
        self.eyebrow = self.story_box.locator("span.eyebrow")
        self.headline = self.story_box.get_by_role("heading")
        self.description = self.story_box.locator("p")

        self.story_card = self.story_box.locator("div.story-card")

        self.tagline = self.story_box.locator("small")
