import pytest
from playwright.sync_api import Page

from src.ui.pages.login import LoginPage
from src.ui.pages.register import RegisterPage
from src.ui.pages.tasks_dashboard import TasksDashboardPage


@pytest.fixture
def login_page(browser_page: Page) -> LoginPage:
    return LoginPage(browser_page)


@pytest.fixture
def register_page(browser_page: Page) -> RegisterPage:
    return RegisterPage(browser_page)


@pytest.fixture
def dashboard_page(authorized_page: Page) -> TasksDashboardPage:
    return TasksDashboardPage(authorized_page)
