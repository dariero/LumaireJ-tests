"""API tests for the journal endpoint."""

from collections.abc import Callable, Generator
from typing import Any

import pytest
import requests

from tests.api.clients.api_client import APIClient
from tests.api.schemas.journal_schema import JournalEntryResponse
from tests.shared.test_data import JournalEntryData

type _CreateFn = Callable[[str, str], tuple[int, dict[str, Any]]]


@pytest.fixture
def journal_entry_factory(api_client: APIClient) -> Generator[_CreateFn]:
    """Create journal entries and guarantee deletion after the test."""
    created_ids: list[str] = []

    def _create(content: str, mood: str = "") -> tuple[int, dict[str, Any]]:
        status_code, body = api_client.create_journal_entry(content, mood)
        created_ids.append(str(body["id"]))
        return status_code, body

    yield _create

    for entry_id in created_ids:
        api_client.delete_journal_entry(entry_id)


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.smoke
def test_create_journal_entry_returns_created_status(
    journal_entry_factory: _CreateFn, journal_entry_data: JournalEntryData
) -> None:
    """Test that creating a journal entry returns 201 Created with valid data."""
    status_code, result = journal_entry_factory(journal_entry_data.content)

    assert status_code == 201, f"Expected 201 Created, got {status_code}"
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_data.content
    assert entry.mood is None


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.smoke
def test_create_journal_entry_with_mood_returns_mood(
    journal_entry_factory: _CreateFn, journal_entry_data: JournalEntryData
) -> None:
    """Test that creating a journal entry with mood returns the mood in response."""
    status_code, result = journal_entry_factory(journal_entry_data.content, journal_entry_data.mood)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_data.content
    assert entry.mood == journal_entry_data.mood


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_without_mood_returns_null_mood(
    journal_entry_factory: _CreateFn, journal_entry_without_mood: JournalEntryData
) -> None:
    """Test that creating a journal entry without mood returns null mood."""
    status_code, result = journal_entry_factory(journal_entry_without_mood.content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == journal_entry_without_mood.content
    assert entry.mood is None


@pytest.mark.xfail(
    reason="SUT returns 422 (FastAPI validation), test expects 400 — see issue #32",
    strict=True,
)
@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_empty_content_fails(api_client: APIClient) -> None:
    """Test that creating a journal entry with empty content returns 400."""
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_journal_entry("")

    assert exc_info.value.response.status_code == 400


@pytest.mark.xfail(
    reason="SUT rejects 10 000-char content with 422 — length constraint added, see issue #33",
    strict=True,
)
@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_long_content_succeeds(
    journal_entry_factory: _CreateFn,
) -> None:
    """Test that creating a journal entry with very long content succeeds."""
    long_content = "A" * 10000
    status_code, result = journal_entry_factory(long_content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == long_content


@pytest.mark.api
@pytest.mark.journal
@pytest.mark.regression
def test_create_journal_entry_with_special_characters_succeeds(
    journal_entry_factory: _CreateFn,
) -> None:
    """Test that journal entries handle special characters correctly."""
    special_content = "Test with 'quotes', \"double quotes\", <html>, & ampersands, émojis 🎉"
    status_code, result = journal_entry_factory(special_content)

    assert status_code == 201
    entry = JournalEntryResponse.model_validate(result)
    assert entry.content == special_content
