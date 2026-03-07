"""Shared fixtures for API and E2E tests."""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from tests.api.clients.api_client import APIClient

# Load .env from project root (explicit path for deterministic behavior)
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for API and UI."""
    url = os.getenv("BASE_URL")
    if not url:
        raise ValueError("BASE_URL environment variable must be set")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def api_base_url(base_url: str) -> str:
    """Return the API base URL."""
    return f"{base_url}/api/v1"


@pytest.fixture(scope="session")
def is_ci() -> bool:
    """Check if running in a CI environment."""
    return os.getenv("CI", "false").lower() in ("1", "true")


@pytest.fixture(scope="session")
def api_client(api_base_url: str) -> APIClient:
    """Provide a configured API client instance."""
    return APIClient(api_base_url)
