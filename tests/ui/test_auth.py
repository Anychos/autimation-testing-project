import allure
import pytest

from src.api.fixtures.auth import UserFixture
from src.api.tools.data_generator import fake_en
from src.ui.pages.login import LoginPage
from src.ui.pages.register import RegisterPage
from src.ui.pages.tasks_dashboard import TasksDashboardPage
from tools.allure import Epic, Feature, Severity, Story


@allure.epic(Epic.UI)
@allure.feature(Feature.AUTHORIZATION)
class TestAuthUI:
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.auth
    @allure.story(Story.REGISTRATION)
    @allure.title("Регистрация через UI")
    @allure.severity(Severity.CRITICAL)
    def test_registration_ui_flow(
        self, register_page: RegisterPage, login_page: LoginPage
    ) -> None:
        register_page.open(register_page.URL)
        password = fake_en.password()

        register_page.form.fill_form(
            email=fake_en.email(), password=password, confirm_password=password
        )
        # register_page.form.check_filled_form()
        register_page.form.click_auth_button()

        register_page.check_current_page_url("/login?registered=1")
        login_page.form.check_visibility(is_login_form=True)
        register_page.form.check_success_login_message()

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.auth
    def test_login_ui(
        self, login_page: LoginPage, registered_user: UserFixture
    ) -> None:
        # Arrange
        login_page.open(login_page.URL)

        # Act
        login_page.form.fill_form(registered_user.email, registered_user.password)
        login_page.form.click_auth_button()

        # Assert
        dashboard = TasksDashboardPage(login_page.page)
        dashboard.check_current_page_url(dashboard.URL)
        dashboard.check_user_email(registered_user.email)
