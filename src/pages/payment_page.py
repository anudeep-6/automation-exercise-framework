"""Page object for the Payment page."""

import allure

from src.pages.base_page import BasePage


@allure.feature("Payment")
class PaymentPage(BasePage):
    """Page object for /payment — card details entry and order confirmation."""

    PATH = "/payment"

    PAYMENT_HEADING = "h2.heading:has-text('Payment')"
    NAME_ON_CARD = "input[data-qa='name-on-card']"
    CARD_NUMBER = "input[data-qa='card-number']"
    CVC = "input[data-qa='cvc']"
    EXPIRY_MONTH = "input[data-qa='expiry-month']"
    EXPIRY_YEAR = "input[data-qa='expiry-year']"
    PAY_BUTTON = "button[data-qa='pay-button']"

    @allure.step("Verify payment page is loaded")
    def verify_page_loaded(self) -> None:
        """Assert the Payment heading, card form, and submit button are visible."""
        self.expect_visible(self.PAYMENT_HEADING)
        self.expect_visible(self.NAME_ON_CARD)
        self.expect_visible(self.PAY_BUTTON)

    @allure.step("Enter card details")
    def enter_card_details(
        self,
        name_on_card: str,
        card_number: str,
        cvc: str,
        expiry_month: str,
        expiry_year: str,
    ) -> None:
        """Fill all card fields in the payment form.

        Args:
            name_on_card: Cardholder name as it appears on the card.
            card_number: Full card number string.
            cvc: 3-digit CVC code.
            expiry_month: Expiry month in MM format.
            expiry_year: Expiry year in YYYY format.
        """
        self.fill(self.NAME_ON_CARD, name_on_card)
        self.fill(self.CARD_NUMBER, card_number)
        self.fill(self.CVC, cvc)
        self.fill(self.EXPIRY_MONTH, expiry_month)
        self.fill(self.EXPIRY_YEAR, expiry_year)

    @allure.step("Click Pay and Confirm Order")
    def confirm_order(self) -> None:
        """Submit the payment form and wait for navigation to complete.

        Uses self.timeout from ConfigReader so the wait respects config.json.
        Navigation is confirmed by the caller asserting the next page's state.
        """
        self.click(self.PAY_BUTTON)
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)

    @allure.step("Enter card details and confirm order")
    def fill_and_confirm(
        self,
        name_on_card: str,
        card_number: str,
        cvc: str,
        expiry_month: str,
        expiry_year: str,
    ) -> None:
        """Convenience method: fill card details and submit in one Allure step.

        Args:
            name_on_card: Cardholder name as it appears on the card.
            card_number: Full card number string.
            cvc: 3-digit CVC code.
            expiry_month: Expiry month in MM format.
            expiry_year: Expiry year in YYYY format.
        """
        self.enter_card_details(
            name_on_card=name_on_card,
            card_number=card_number,
            cvc=cvc,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
        )
        self.confirm_order()
