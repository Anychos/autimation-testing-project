from typing import Literal

from playwright.sync_api import Locator, Page, expect

from src.ui.components.create_task_form import CreateTaskForm
from src.ui.components.task_card import TaskCard
from src.ui.pages.base import BasePage
from src.ui.tools.routes import Route


class TasksDashboardPage(BasePage):
    URL = Route.DASHBOARD

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.task_form = CreateTaskForm(page)

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
        self.notification_button = self.topbar.get_by_test_id("notification-bell")
        self.notification_panel = self.topbar.get_by_test_id("notification-panel")
        self.notification_panel_title = self.notification_panel.get_by_role(
            role="heading", level=2
        )
        self.notification_mark_all_as_read_button = (
            self.notification_panel.get_by_test_id("notification-mark-all-read")
        )
        self.notification_error_state_message = self.notification_panel.get_by_test_id(
            "notification-error-state"
        )
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
        self.create_task_success_message = self.task_section.locator("p.success-note")

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

        self.no_results_state = self.task_section.get_by_test_id("no-results")
        self.no_results_title = self.no_results_state.get_by_role("heading")
        self.no_results_description = self.no_results_state.locator("p")
        self.no_results_clear_filters_button = self.no_results_state.get_by_role(
            "button", name="Clear filters", exact=True
        )

        self.list_footer = self.task_section.locator("footer.list-footer")
        self.tasks_count_text = self.list_footer.locator("span.muted")

        self.pagination = self.list_footer.locator("div.pagination")
        self.page_size_select = self.pagination.get_by_test_id("page-size")
        self.previous_page_button = self.pagination.get_by_test_id("previous-page")
        self.current_page = self.pagination.get_by_test_id("current-page")
        self.next_page_button = self.pagination.get_by_test_id("next-page")

        self.clear_filters_button = self.task_section.get_by_role(
            "button", name="Clear filters", exact=True
        )
        self.try_again_button = self.task_section.get_by_role(
            "button", name="Try again", exact=True
        )

    def task_card(self, task_id: str) -> TaskCard:
        return TaskCard(self.page, task_id)

    def page_size_option(self, value: Literal["5", "10", "25", "50"]) -> Locator:
        return self.page_size_select.locator(f"option[value='{value}']")

    def status_option(
        self, value: Literal["todo", "in_progress", "done", ""]
    ) -> Locator:
        return self.status_filter.locator(f"option[value='{value}']")

    def sort_option(
        self, value: Literal["created_desc", "created_asc", "due_date_asc"]
    ) -> Locator:
        return self.sort_select.locator(f"option[value='{value}']")

    def open_tasks(self) -> None:
        self.active_tab.click()

    def logout(self) -> None:
        self.logout_button.click()

    def open_create_task(self) -> None:
        self.create_task_button.click()

    def open_create_task_from_empty_state(self) -> None:
        self.empty_state_create_button.click()

    def input_search(self, query: str) -> None:
        self.search_input.fill(query)

    def clear_search(self) -> None:
        self.search_input.clear()

    def select_status(self, status: Literal["todo", "in_progress", "done", ""]) -> None:
        self.status_filter.select_option(status)

    def select_sort(
        self, sort: Literal["created_desc", "created_asc", "due_date_asc"]
    ) -> None:
        self.sort_select.select_option(sort)

    def clear_filters(self) -> None:
        self.clear_filters_button.click()

    def retry_load(self) -> None:
        self.try_again_button.click()

    def select_page_size(self, size: Literal["5", "10", "25", "50"]) -> None:
        self.page_size_select.select_option(size)

    def go_to_previous_page(self) -> None:
        self.previous_page_button.click()

    def go_to_next_page(self) -> None:
        self.next_page_button.click()

    def check_task_visible(self, task_id: str, heading: str) -> None:
        card = self.task_card(task_id)
        expect(card.card).to_be_visible()
        card.check_title(heading)

    def check_user_email(self, email: str) -> None:
        expect(self.user_email).to_have_text(email)

    def confirm_delete_task(self) -> None:
        self.page.get_by_test_id("delete-confirm").click()

    def check_task_absent(self, task_id: str) -> None:
        expect(self.task_card(task_id).card).to_have_count(0)

    def check_empty_state(self) -> None:
        expect(self.empty_state_title).to_be_visible()
        expect(self.empty_state_description).to_be_visible()
        expect(self.empty_state_create_button).to_be_visible()

    def check_no_results_state(self) -> None:
        expect(self.no_results_title).to_be_visible()
        expect(self.no_results_description).to_be_visible()
        expect(self.no_results_clear_filters_button).to_be_visible()
