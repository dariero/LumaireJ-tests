"""E2E tests for the journaling UI."""

import pytest

from tests.e2e.pages.journal_page import JournalPage
from tests.shared.test_data import JournalEntryData


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.smoke
def test_journal_submission_with_mood_saves_entry(
    journal_page: JournalPage, journal_entry_data: JournalEntryData
) -> None:
    """Test that submitting a journal entry with mood saves successfully."""
    journal_page.fill(content=journal_entry_data.content, mood=journal_entry_data.mood)
    journal_page.submit()
    journal_page.expect_success()


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.smoke
def test_journal_submission_without_mood_saves_entry(
    journal_page: JournalPage, journal_entry_without_mood: JournalEntryData
) -> None:
    """Test that submitting a journal entry without mood saves successfully."""
    journal_page.fill(content=journal_entry_without_mood.content)
    journal_page.submit()
    journal_page.expect_success()


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.regression
def test_journal_submission_success_message(
    journal_page: JournalPage, journal_entry_data: JournalEntryData
) -> None:
    """Test that a success message appears after submission."""
    journal_page.fill(content=journal_entry_data.content, mood=journal_entry_data.mood)
    journal_page.submit()

    response_text = journal_page.get_response_text()
    assert "Saved" in response_text
    assert "id:" in response_text


@pytest.mark.e2e
@pytest.mark.journal
@pytest.mark.regression
def test_journal_form_validation_prevents_empty_submission(journal_page: JournalPage) -> None:
    """Test that form validation prevents submission with empty content."""
    journal_page.submit()

    assert not journal_page.is_response_visible(timeout=500), (
        "Response element should not be visible for empty form"
    )
