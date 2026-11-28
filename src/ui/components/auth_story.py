from playwright.sync_api import Page, expect

from src.ui.components.base import BaseComponent


class AuthStory(BaseComponent):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.story_box = self.page.locator("section.auth-story")

        self.brand = self.story_box.locator("span.brand")
        self.headline = self.story_box.get_by_role("heading")
        self.description = self.story_box.locator("p")

        self.story_card = self.story_box.locator("div.story-card")

    def check_visibility(self) -> None:
        expect(self.brand).to_be_visible()
        expect(self.brand).to_contain_text("TaskFlow.")

        expect(self.headline).to_be_visible()
        expect(self.headline).to_contain_text("Make room for what matters.")

        expect(self.description).to_be_visible()
        expect(self.description).to_contain_text(
            "Your plans, your pace. Keep everything you need to do in one calm, simple space."
        )

        expect(self.story_card).to_be_visible()
