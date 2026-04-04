"""This file contains the RegistrationPage class."""

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
    NAME_INPUT = "input[data-qa='name']"
    EMAIL_INPUT = "input[data-qa='email']"
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

    def expect_account_info_form_visible(self):
        """Asserts 'Enter Account Information' heading is visible."""
        self.expect_visible(self.ACCOUNT_INFO_HEADING)

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

    def enter_password(self, password: str):
        """Fills the password field."""
        self.fill(self.PASSWORD_INPUT, password)

    def select_date_of_birth(self, day: str, month: str, year: str):
        """Selects day, month, year from the date of birth dropdowns.

        Args:
            day (str): Day value e.g. '15'
            month (str): Month value e.g. '6' for June
            year (str): Year value e.g. '1990'
        """
        self.page.locator(self.DAYS_SELECT).select_option(day)
        self.page.locator(self.MONTHS_SELECT).select_option(month)
        self.page.locator(self.YEARS_SELECT).select_option(year)

    def select_newsletter(self):
        """Checks the newsletter checkbox if not already checked."""
        if not self.page.locator(self.NEWSLETTER_CHECKBOX).is_checked():
            self.click(self.NEWSLETTER_CHECKBOX)

    def select_optin(self):
        """Checks the special offers checkbox if not already checked."""
        if not self.page.locator(self.OPTIN_CHECKBOX).is_checked():
            self.click(self.OPTIN_CHECKBOX)

    def enter_first_name(self, first_name: str):
        """Fills the first name field."""
        self.fill(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name: str):
        """Fills the last name field."""
        self.fill(self.LAST_NAME_INPUT, last_name)

    def enter_company(self, company: str):
        """Fills the company field."""
        self.fill(self.COMPANY_INPUT, company)

    def enter_address(self, address: str):
        """Fills the primary address field."""
        self.fill(self.ADDRESS_INPUT, address)

    def enter_address2(self, address2: str):
        """Fills the secondary address field."""
        self.fill(self.ADDRESS2_INPUT, address2)

    def select_country(self, country: str):
        """Selects country from dropdown.

        Args:
            country (str): Country name e.g. 'India', 'United States'
        """
        self.page.locator(self.COUNTRY_SELECT).select_option(country)

    def enter_state(self, state: str):
        """Fills the state field."""
        self.fill(self.STATE_INPUT, state)

    def enter_city(self, city: str):
        """Fills the city field."""
        self.fill(self.CITY_INPUT, city)

    def enter_zipcode(self, zipcode: str):
        """Fills the zipcode field."""
        self.fill(self.ZIPCODE_INPUT, zipcode)

    def enter_mobile(self, mobile: str):
        """Fills the mobile number field."""
        self.fill(self.MOBILE_INPUT, mobile)

    def submit_create_account(self):
        """Clicks the Create Account button."""
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def fill_account_info(
        self, title: str, password: str, day: str, month: str, year: str
    ):
        """Fills the entire account information section.

        Args:
            title: 'Mr' or 'Mrs'
            password: Account password
            day: Birth day e.g. '15'
            month: Birth month e.g. '6'
            year: Birth year e.g. '1990'
        """
        self.select_title(title)
        self.enter_password(password)
        self.select_date_of_birth(day, month, year)
        self.select_newsletter()
        self.select_optin()

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
