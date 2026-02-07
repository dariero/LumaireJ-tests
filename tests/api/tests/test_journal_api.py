"""Simple API tests using Faker for test data."""

from datetime import datetime

import pytest
import requests

from tests.api.clients.api_client import APIClient
from tests.api.schemas.journal_schema import JournalEntryResponse
from tests.shared.test_data import JournalEntryData


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.smoke
def test_create_journal_entry_returns_created_status(
    api_client: APIClient, journal_entry_data: JournalEntryData
) -> None:
    """Test that creating a journal entry returns 201 Created with valid data."""
    status_code, result = api_client.create_journal_entry(journal_entry_data.content)

    # Assert HTTP status code
    assert status_code == 201, f"Expected 201 Created, got {status_code}"

    # Validate response body
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_data.content
    assert isinstance(entry.id, int)
    assert entry.id > 0
    assert isinstance(entry.created_at, datetime)
    assert entry.mood is None

    # Cleanup
    api_client.delete_journal_entry(str(entry.id))


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.smoke
def test_create_journal_entry_with_mood_returns_mood(
    api_client: APIClient, journal_entry_data: JournalEntryData
) -> None:
    """Test that creating a journal entry with mood returns the mood in response."""
    status_code, result = api_client.create_journal_entry(
        journal_entry_data.content, journal_entry_data.mood
    )

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_data.content
    assert entry.mood == journal_entry_data.mood
    assert isinstance(entry.id, int)
    assert entry.id > 0
    assert isinstance(entry.created_at, datetime)

    # Cleanup
    api_client.delete_journal_entry(str(entry.id))


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_without_mood_returns_null_mood(
    api_client: APIClient, journal_entry_without_mood: JournalEntryData
) -> None:
    """Test that creating a journal entry without mood returns null mood."""
    status_code, result = api_client.create_journal_entry(journal_entry_without_mood.content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_without_mood.content
    assert entry.mood is None
    assert isinstance(entry.id, int)
    assert entry.id > 0
    assert isinstance(entry.created_at, datetime)

    # Cleanup
    api_client.delete_journal_entry(str(entry.id))


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_empty_content_fails(api_client: APIClient) -> None:
    """Test that creating a journal entry with empty content returns 400."""
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_journal_entry("")

    assert exc_info.value.response.status_code == 400


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_long_content_succeeds(api_client: APIClient) -> None:
    """Test that creating a journal entry with very long content succeeds."""
    long_content = "A" * 10000
    status_code, result = api_client.create_journal_entry(long_content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == long_content

    # Cleanup
    api_client.delete_journal_entry(str(entry.id))


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_special_characters_succeeds(
    api_client: APIClient,
) -> None:
    """Test that journal entries handle special characters correctly."""
    special_content = "Test with 'quotes', \"double quotes\", <html>, & ampersands, émojis 🎉"
    status_code, result = api_client.create_journal_entry(special_content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == special_content

    # Cleanup
    api_client.delete_journal_entry(str(entry.id))
