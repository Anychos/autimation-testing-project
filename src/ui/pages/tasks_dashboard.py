from typing import Literal

from playwright.sync_api import Locator, Page

from src.ui.pages.base import BasePage


class TasksDashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.sidebar = self.page.locator("aside.sidebar")
        self.brand = self.sidebar.locator("span.brand")
        self.sidebar_label = self.sidebar.locator("span.sidebar-label")
        self.active_tab = self.sidebar.locator("a.nav-active")
        self.tab_tasks_counter = self.active_tab.locator("span.nav-count")
        self.sidebar_footer = self.sidebar.locator("div.sidebar-footer")
        self.sidebar_footer_title = self.sidebar_footer.locator("strong")
        self.sidebar_footer_subtitle = self.sidebar_footer.locator("p")

        self.topbar = self.page.locator("header.topbar")
        self.breadcrumb = self.topbar.locator("span.breadcrumb")
        self.user_avatar = self.topbar.locator("span.avatar")
        self.user_email = self.topbar.get_by_test_id("current-user-email")
        self.logout_button = self.topbar.get_by_test_id("logout-button")

        self.dashboard = self.page.locator("main.dashboard")

        self.page_heading = self.dashboard.locator("div.page-heading")
        self.headline = self.page_heading.get_by_role("heading", level=1)
        self.description = self.page_heading.locator("p.muted")
        self.create_task_button = self.page_heading.get_by_test_id("create-task-button")

        self.stats = self.dashboard.locator("section.stats")
        self.total_count = self.stats.get_by_test_id("total-count")
        self.in_progress_count = self.stats.get_by_test_id("in-progress-count")
        self.completed_count = self.stats.get_by_test_id("completed-count")

        self.total_label = self.stats.get_by_text("Total tasks", exact=True)
        self.in_progress_label = self.stats.get_by_text("In Progress", exact=True)
        self.completed_label = self.stats.get_by_text("Completed", exact=True)

        self.task_section = self.dashboard.locator("section.task-section")
        self.list_heading = self.task_section.locator("div.list-heading")
        self.list_title = self.list_heading.get_by_role("heading")
        self.list_count = self.list_heading.locator("span.pill")

        self.toolbar = self.task_section.locator("div.toolbar")
        self.search_input = self.toolbar.get_by_test_id("task-search")
        self.status_filter = self.toolbar.get_by_test_id("status-filter")
        self.sort_select = self.toolbar.get_by_test_id("sort-select")

        self.empty_state = self.task_section.get_by_test_id("empty-tasks")
        self.empty_state_title = self.empty_state.get_by_role("heading")
        self.empty_state_description = self.empty_state.locator("p")
        self.empty_state_create_button = self.empty_state.get_by_role(
            "button", name="Create Task", exact=True
        )

        self.list_footer = self.task_section.locator("footer.list-footer")
        self.tasks_count_text = self.list_footer.locator("span.muted")

        self.pagination = self.list_footer.locator("div.pagination")
        self.page_size_select = self.pagination.get_by_test_id("page-size")
        self.previous_page_button = self.pagination.get_by_test_id("previous-page")
        self.current_page = self.pagination.get_by_test_id("current-page")
        self.next_page_button = self.pagination.get_by_test_id("next-page")

    def page_size_option(self, value: Literal["5", "10", "25", "50"]) -> Locator:
        return self.page_size_select.locator(f"option[value='{value}']")
