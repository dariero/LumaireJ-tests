"""Simple Page Object Model for the journaling page."""

from playwright.sync_api import Page, expect

from tests.shared.constants import DEFAULT_TIMEOUT_MS


class JournalPage:
    """Page Object Model for the journaling page."""

    BASE_PATH = "/static/journal.html"

    # Selectors
    CONTENT = "#content"
    MOOD = "#mood"
    SUBMIT = "button[type=submit]"
    RESPONSE = "#response"

    def __init__(self, page: Page, base_url: str) -> None:
        """Initialize the Page Object."""
        self.page = page
        self.url = f"{base_url.rstrip('/')}{self.BASE_PATH}"

    def open(self) -> None:
        """Navigate to the journaling page."""
        self.page.goto(self.url, wait_until="load")
        # Verify page loaded by checking form is present
        expect(self.page.locator(self.CONTENT)).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)

    def fill(self, content: str, mood: str = "") -> None:
        """Fill out the journaling form."""
        self.page.locator(self.CONTENT).fill(content)
        if mood:
            self.page.locator(self.MOOD).fill(mood)

    def submit(self) -> None:
        """Submit the journaling form."""
        self.page.locator(self.SUBMIT).click()

    def expect_success(self) -> None:
        """Assert that a success message appears."""
        locator = self.page.locator(self.RESPONSE)
        expect(locator).to_contain_text("Saved", timeout=DEFAULT_TIMEOUT_MS)

    def get_response_text(self) -> str:
        """Get the text from the response element."""
        response_locator = self.page.locator(self.RESPONSE)

        response_locator.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)

        text = response_locator.text_content() or ""
        return text

    def is_response_visible(self, timeout: int = 1000) -> bool:
        """Check if a response element is visible.

        Args:
            timeout: Maximum time to wait in milliseconds (default: 1000ms)

        Returns:
            bool: True if visible, False otherwise
        """
        response_locator = self.page.locator(self.RESPONSE)
        try:
            response_locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
