from playwright.sync_api import Page, expect

from src.ui.components.base_form import BaseForm


class AuthForm(BaseForm):
    def __init__(self, page: Page) -> None:
        super().__init__(page, form_box=page.locator("div.auth-box"))

        self.email_label = self.form_box.locator("label[for='email']")
        self.email_input = self.form_box.get_by_test_id("email-input")
        self.password_label = self.form_box.locator("label[for='password']")
        self.password_input = self.form_box.get_by_test_id("password-input")
        self.confirm_password_label = self.form_box.locator("label[for='confirmation']")
        self.confirm_password_input = self.form_box.get_by_test_id(
            "confirm-password-input"
        )

        self.auth_button = self.form_box.get_by_test_id("auth-submit")

        self.switch_form_text = self.form_box.locator("p.auth-switch")
        self.switch_form_link = self.form_box.get_by_test_id("auth-switch")

        self.success_login_message = self.form_box.locator("p.notice")

    def check_visibility(self, *, is_login_form: bool) -> None:
        expect(self.email_label).to_be_visible()
        expect(self.email_label).to_have_text("Email")

        expect(self.email_input).to_be_visible()

        expect(self.password_label).to_be_visible()
        expect(self.password_label).to_have_text("Password")

        expect(self.password_input).to_be_visible()

        expect(self.auth_button).to_be_visible()

        expect(self.switch_form_text).to_be_visible()

        if is_login_form == True:
            expect(self.form_title).to_be_visible()
            expect(self.form_title).to_have_text("Welcome back")

            expect(self.title_subtext).to_be_visible()
            expect(self.title_subtext).to_have_text("Let’s pick up where you left off.")

            expect(self.switch_form_text).to_have_text(
                "New to TaskFlow? Create an account"
            )

        if is_login_form == False:
            expect(self.form_title).to_be_visible()
            expect(self.form_title).to_have_text("Create your account")

            expect(self.title_subtext).to_be_visible()
            expect(self.title_subtext).to_have_text(
                "A fresh start for your everyday plans."
            )

            expect(self.field_label("confirmation")).to_be_visible()
            expect(self.field_label("confirmation")).to_have_text("Confirm password")

            expect(self.confirm_password_input).to_be_visible()

            expect(self.switch_form_text).to_have_text(
                "Already have an account? Sign in"
            )

    def fill_form(
        self,
        email: str,
        password: str,
        confirm_password: str | None = None,
    ) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)

        if confirm_password is not None:
            self.confirm_password_input.fill(confirm_password)

    def check_email_error(self) -> None:
        message = "Enter a valid email address."
        self.check_field_error("email", message)

    def check_password_error(self) -> None:
        message = "Use 8–64 characters."
        self.check_field_error("password", message)

    def clear_email_input(self) -> None:
        self.email_input.clear()

    def clear_password_input(self) -> None:
        self.password_input.clear()

    def clear_confirm_password_input(self) -> None:
        self.confirm_password_input.clear()

    def click_auth_button(self) -> None:
        self.auth_button.click()

    def click_switch_form_link(self) -> None:
        self.switch_form_link.click()

    def check_success_login_message(self) -> None:
        expect(self.success_login_message).to_be_visible()
        expect(self.success_login_message).to_have_text(
            "Account created. Sign in to continue."
        )
