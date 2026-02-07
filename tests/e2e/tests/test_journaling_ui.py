"""Simple E2E tests using Faker for test data."""

import pytest
from playwright.sync_api import Page

from tests.e2e.pages.journal_page import JournalPage
from tests.shared.test_data import JournalEntryData


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.smoke
def test_journal_submission_with_mood_saves_entry(
    page: Page, ui_base_url: str, journal_entry_data: JournalEntryData
) -> None:
    """Test that submitting a journal entry with mood saves successfully."""
    journal = JournalPage(page, ui_base_url)
    journal.open()
    journal.fill(content=journal_entry_data.content, mood=journal_entry_data.mood)
    journal.submit()
    journal.expect_success()


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.smoke
def test_journal_submission_without_mood_saves_entry(
    page: Page, ui_base_url: str, journal_entry_without_mood: JournalEntryData
) -> None:
    """Test that submitting a journal entry without mood saves successfully."""
    journal = JournalPage(page, ui_base_url)
    journal.open()
    journal.fill(content=journal_entry_without_mood.content)
    journal.submit()
    journal.expect_success()


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.regression
def test_journal_submission_success_message(
    page: Page, ui_base_url: str, journal_entry_data: JournalEntryData
) -> None:
    """Test that a success message appears after submission."""
    journal = JournalPage(page, ui_base_url)
    journal.open()
    journal.fill(content=journal_entry_data.content, mood=journal_entry_data.mood)
    journal.submit()

    response_text = journal.get_response_text()
    assert "Saved" in response_text
    assert "id:" in response_text


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.regression
def test_journal_form_validation_prevents_empty_submission(page: Page, ui_base_url: str) -> None:
    """Test that form validation prevents submission with empty content."""
    journal = JournalPage(page, ui_base_url)
    journal.open()

    # Try to submit an empty form
    journal.submit()

    # Wait briefly to ensure no response appears
    page.wait_for_timeout(500)

    assert not journal.is_response_visible(timeout=500), (
        "Response element should not be visible for empty form"
    )
