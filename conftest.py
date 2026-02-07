"""Main test configuration with shared fixtures."""

# Import shared fixtures for pytest discovery
from tests.shared.fixtures import (  # noqa: F401
    api_base_url,
    api_client,
    base_url,
    is_ci,
    ui_base_url,
)
from tests.shared.test_data import (  # noqa: F401
    journal_entry_data,
    journal_entry_without_mood,
)
