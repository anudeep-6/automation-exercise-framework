"""This page contains ContactUsPage class"""

import allure

from src.pages.base_page import BasePage
from src.utils.exceptions import DialogException


class ContactUsPage(BasePage):
    """Page object for the Contact Us page (/contact_us).

    Provides interactions for filling out and submitting the contact form,
    including file upload and dialog handling.
    """

    PATH = "/contact_us"

    GET_IN_TOUCH_FORM = "h2:has-text('Get In Touch')"
    NAME = "input[data-qa='name']"
    EMAIL = "input[data-qa='email']"
    SUBJECT = "input[data-qa='subject']"
    MESSAGE = "textarea[data-qa='message']"
    CHOOSE_FILE_BUTTON = "input[name='upload_file']"
    SUBMIT_BUTTON = "input[data-qa='submit-button']"
    SUCCESS_MESSAGE = "div.status.alert.alert-success"
    HOME_BUTTON = "#form-section a.btn-success"

    @allure.step("Expect Get In Touch form is visible")
    def expect_get_in_touch_form_visible(self) -> None:
        """Asserts the 'Get In Touch' form heading is visible."""
        self.expect_visible(self.GET_IN_TOUCH_FORM)

    @allure.step("Enter name: {name}")
    def enter_name(self, name: str) -> None:
        """Fills the name field in the contact form.

        Args:
            name (str): Contact name.
        """
        self.fill(self.NAME, name)

    @allure.step("Enter email: {email}")
    def enter_email(self, email: str) -> None:
        """Fills the email field in the contact form.

        Args:
            email (str): Contact email address.
        """
        self.fill(self.EMAIL, email)

    @allure.step("Enter subject: {subject}")
    def enter_subject(self, subject: str) -> None:
        """Fills the subject field in the contact form.

        Args:
            subject (str): Message subject.
        """
        self.fill(self.SUBJECT, subject)

    @allure.step("Enter message")
    def enter_message(self, message: str) -> None:
        """Fills the message textarea in the contact form.

        Args:
            message (str): Message body.
        """
        self.fill(self.MESSAGE, message)

    @allure.step("Upload file attachment: {file_path}")
    def upload_file_attachment(self, file_path: str) -> None:
        """Uploads a file via the file upload input.

        Args:
            file_path (str): Absolute path to the file to upload.
        """
        self.upload_file(self.CHOOSE_FILE_BUTTON, file_path)

    @allure.step("Fill contact us form for: {name}")
    def fill_contact_us_form(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
        file_path: str,
    ) -> None:
        """Fills all fields of the contact form and uploads a file.

        Args:
            name (str): Contact name.
            email (str): Contact email address.
            subject (str): Message subject.
            message (str): Message body.
            file_path (str): Absolute path to file to upload.
        """
        self.enter_name(name)
        self.enter_email(email)
        self.enter_subject(subject)
        self.enter_message(message)
        self.upload_file_attachment(file_path)

    @allure.step("Submit contact form and accept confirmation dialog")
    def submit_and_accept_dialog(self) -> str:
        """Click the Submit button and accept the browser confirm dialog.

        The contact form triggers a native browser confirm() dialog on submit.
        Playwright requires the dialog handler to be registered before the
        click that triggers it, which this method handles internally.

        Returns:
            str: The message text from the dialog (e.g. 'Press OK to proceed!').

        Raises:
            DialogException: If no dialog was triggered after the submit click.
        """

        dialog_message = self.accept_dialog()
        self.click(self.SUBMIT_BUTTON)
        # give the dialog a moment to fire
        self.page.wait_for_timeout(1500)
        if not dialog_message:
            raise DialogException("click submit button on contact form")
        return dialog_message[0]

    @allure.step("Expect success message is visible")
    def expect_success_message_visible(self) -> None:
        """Asserts the success message is visible after form submission."""
        self.expect_visible(self.SUCCESS_MESSAGE)

    @allure.step("Click Home button")
    def click_home_button(self) -> None:
        """Clicks the Home button to return to the home page."""
        self.click(self.HOME_BUTTON)
