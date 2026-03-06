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
        expect(self.page.locator(self.CONTENT)).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)

    def fill(self, content: str, mood: str = "") -> None:
        """Fill out the journaling form."""
        content_locator = self.page.locator(self.CONTENT)
        expect(content_locator).to_be_enabled(timeout=DEFAULT_TIMEOUT_MS)
        content_locator.fill(content)
        if mood:
            mood_locator = self.page.locator(self.MOOD)
            expect(mood_locator).to_be_enabled(timeout=DEFAULT_TIMEOUT_MS)
            mood_locator.fill(mood)

    def submit(self) -> None:
        """Submit the journaling form."""
        self.page.locator(self.SUBMIT).click()

    def expect_success(self) -> None:
        """Assert that a success message appears."""
        locator = self.page.locator(self.RESPONSE)
        expect(locator).to_contain_text("Saved", timeout=DEFAULT_TIMEOUT_MS)

    def get_response_text(self) -> str:
        """Get the text from the response element.

        Waits for the element to be visible before reading, then returns its
        inner text. Uses inner_text() which reflects rendered CSS visibility,
        unlike text_content() which reads the DOM regardless of display state.
        """
        response_locator = self.page.locator(self.RESPONSE)
        expect(response_locator).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
        return response_locator.inner_text()

    def is_response_visible(self, timeout: int = 1000) -> bool:
        """Check if the response element is visible within the given timeout.

        Args:
            timeout: Maximum time to wait in milliseconds (default: 1000ms).

        Returns:
            True if visible within timeout, False otherwise.
        """
        try:
            expect(self.page.locator(self.RESPONSE)).to_be_visible(timeout=timeout)
            return True
        except AssertionError:
            return False
