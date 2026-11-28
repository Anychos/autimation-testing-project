from http import HTTPStatus
from typing import Any

import pytest
from playwright.sync_api import BrowserContext, Page
from pytest_playwright.pytest_playwright import CreateContextCallback

from src.api.assertions.base import assert_status_code
from src.api.config import settings
from src.api.fixtures.auth import UserFixture
from src.api.tools.routes import Route


@pytest.fixture
def browser_page(page: Page) -> Page:
    return page


@pytest.fixture
def browser_state(
    new_context: CreateContextCallback,
    registered_user: UserFixture,
) -> dict[str, Any]:
    context: BrowserContext = new_context()

    try:
        response = context.request.post(
            f"{settings.http_client.url}{Route.LOGIN}",
            data=registered_user.login_data.model_dump(mode="json"),
            headers={
                "Origin": settings.http_client.url,
            },
        )

        assert_status_code(
            expected=HTTPStatus.OK,
            actual=response.status,
        )

        return context.storage_state()

    finally:
        context.close()


@pytest.fixture
def authorized_page(
    new_context: CreateContextCallback,
    browser_state: dict[str, Any],
) -> Page:
    context = new_context(storage_state=browser_state)

    return context.new_page()
