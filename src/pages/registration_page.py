"""This file contains the RegistrationPage class."""

import allure

from src.pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Page object for the Account Registration page (/signup).

    Covers account information, date of birth, checkboxes,
    and address information sections.
    """

    PATH = "/signup"

    ACCOUNT_INFO_HEADING = "h2:has-text('Enter Account Information')"
    TITLE_MR = "input[id='id_gender1']"
    TITLE_MRS = "input[id='id_gender2']"
    PASSWORD_INPUT = "input[data-qa='password']"
    DAYS_SELECT = "select[data-qa='days']"
    MONTHS_SELECT = "select[data-qa='months']"
    YEARS_SELECT = "select[data-qa='years']"
    NEWSLETTER_CHECKBOX = "input[id='newsletter']"
    OPTIN_CHECKBOX = "input[id='optin']"
    FIRST_NAME_INPUT = "input[data-qa='first_name']"
    LAST_NAME_INPUT = "input[data-qa='last_name']"
    COMPANY_INPUT = "input[data-qa='company']"
    ADDRESS_INPUT = "input[data-qa='address']"
    ADDRESS2_INPUT = "input[data-qa='address2']"
    COUNTRY_SELECT = "select[data-qa='country']"
    STATE_INPUT = "input[data-qa='state']"
    CITY_INPUT = "input[data-qa='city']"
    ZIPCODE_INPUT = "input[data-qa='zipcode']"
    MOBILE_INPUT = "input[data-qa='mobile_number']"
    CREATE_ACCOUNT_BUTTON = "button[data-qa='create-account']"

    @allure.step("Expect account information form is visible")
    def expect_account_info_form_visible(self):
        """Asserts 'Enter Account Information' heading is visible."""
        self.expect_visible(self.ACCOUNT_INFO_HEADING)

    @allure.step("Select title")
    def select_title(self, title: str):
        """Selects Mr or Mrs radio button.

        Args:
            title (str): 'Mr' or 'Mrs'
        """
        if title == "Mr":
            self.click(self.TITLE_MR)
        elif title == "Mrs":
            self.click(self.TITLE_MRS)
        else:
            raise ValueError(f"Invalid title '{title}'. Must be 'Mr' or 'Mrs'")

    @allure.step("Enter password")
    def enter_password(self, password: str):
        """Fills the password field."""
        self.fill(self.PASSWORD_INPUT, password)

    @allure.step("Select date of birth")
    def select_date_of_birth(self, day: str, month: str, year: str):
        """Selects day, month, year from the date of birth dropdowns.

        Args:
            day (str): Day value e.g. '15'
            month (str): Month value e.g. '6' for June
            year (str): Year value e.g. '1990'
        """
        self.select_option(self.DAYS_SELECT, day)
        self.select_option(self.MONTHS_SELECT, month)
        self.select_option(self.YEARS_SELECT, year)

    @allure.step("Select newsletter subscription")
    def select_newsletter(self):
        """Checks the newsletter checkbox if not already checked."""
        if not self.is_checked(self.NEWSLETTER_CHECKBOX):
            self.click(self.NEWSLETTER_CHECKBOX)

    @allure.step("Select special offers opt-in")
    def select_optin(self):
        """Checks the special offers checkbox if not already checked."""
        if not self.is_checked(self.OPTIN_CHECKBOX):
            self.click(self.OPTIN_CHECKBOX)

    @allure.step("Enter first name")
    def enter_first_name(self, first_name: str):
        """Fills the first name field."""
        self.fill(self.FIRST_NAME_INPUT, first_name)

    @allure.step("Enter last name")
    def enter_last_name(self, last_name: str):
        """Fills the last name field."""
        self.fill(self.LAST_NAME_INPUT, last_name)

    @allure.step("Enter company")
    def enter_company(self, company: str):
        """Fills the company field."""
        self.fill(self.COMPANY_INPUT, company)

    @allure.step("Enter address")
    def enter_address(self, address: str):
        """Fills the primary address field."""
        self.fill(self.ADDRESS_INPUT, address)

    @allure.step("Enter secondary address")
    def enter_address2(self, address2: str):
        """Fills the secondary address field."""
        self.fill(self.ADDRESS2_INPUT, address2)

    @allure.step("Select country")
    def select_country(self, country: str):
        """Selects country from dropdown.

        Args:
            country (str): Country name e.g. 'India', 'United States'
        """
        self.select_option(self.COUNTRY_SELECT, country)

    @allure.step("Enter state")
    def enter_state(self, state: str):
        """Fills the state field."""
        self.fill(self.STATE_INPUT, state)

    @allure.step("Enter city")
    def enter_city(self, city: str):
        """Fills the city field."""
        self.fill(self.CITY_INPUT, city)

    @allure.step("Enter zipcode")
    def enter_zipcode(self, zipcode: str):
        """Fills the zipcode field."""
        self.fill(self.ZIPCODE_INPUT, zipcode)

    @allure.step("Enter mobile number")
    def enter_mobile(self, mobile: str):
        """Fills the mobile number field."""
        self.fill(self.MOBILE_INPUT, mobile)

    @allure.step("Submit create account form")
    def submit_create_account(self):
        """Clicks the Create Account button."""
        self.click(self.CREATE_ACCOUNT_BUTTON)

    @allure.step("Fill account information")
    def fill_account_info(
        self,
        title: str,
        password: str,
        day: str,
        month: str,
        year: str,
        newsletter: bool = True,
        optin: bool = True,
    ):
        """Fills the entire account information section.

        Args:
            title: 'Mr' or 'Mrs'
            password: Account password
            day: Birth day e.g. '15'
            month: Birth month e.g. '6'
            year: Birth year e.g. '1990'
            newsletter: Whether to check the newsletter checkbox. Defaults to True.
            optin: Whether to check the special offers checkbox. Defaults to True.
        """
        self.select_title(title)
        self.enter_password(password)
        self.select_date_of_birth(day, month, year)
        if newsletter:
            self.select_newsletter()
        if optin:
            self.select_optin()

    @allure.step("Fill address information")
    def fill_address_info(
        self,
        first_name: str,
        last_name: str,
        address: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile: str,
        company: str = "",
        address2: str = "",
    ):
        """Fills the entire address information section.

        Args:
            first_name: First name
            last_name: Last name
            address: Primary street address
            country: Country name
            state: State name
            city: City name
            zipcode: Zip/postal code
            mobile: Mobile number
            company: Optional company name
            address2: Optional secondary address line
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        if company:
            self.enter_company(company)
        self.enter_address(address)
        if address2:
            self.enter_address2(address2)
        self.select_country(country)
        self.enter_state(state)
        self.enter_city(city)
        self.enter_zipcode(zipcode)
        self.enter_mobile(mobile)
