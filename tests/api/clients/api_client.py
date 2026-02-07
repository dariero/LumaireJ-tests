"""Simple API client for endpoints."""

import json
from typing import Any

import requests

from tests.shared.constants import API_REQUEST_TIMEOUT_SEC


class APIClient:
    """Simple client for API endpoints."""

    def __init__(self, base_url: str) -> None:
        """Initialize the API client."""
        self.base_url = base_url.rstrip("/")

    def create_journal_entry(self, content: str, mood: str = "") -> tuple[int, dict[str, Any]]:
        """Create a new journal entry.

        Returns:
            tuple: (status_code, response_body)

        Raises:
            requests.exceptions.RequestException: On connection/timeout errors
            ValueError: On non-JSON response
        """
        payload: dict[str, str] = {"content": content}
        if mood:
            payload["mood"] = mood

        url: str = f"{self.base_url}/journal"

        try:
            response = requests.post(url, json=payload, timeout=API_REQUEST_TIMEOUT_SEC)
        except requests.exceptions.RequestException as exc:
            raise requests.exceptions.RequestException(
                f"Failed to POST {url} with payload {payload}: {exc}"
            ) from exc

        try:
            body = response.json()
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Non-JSON response from {url} (status {response.status_code}): "
                f"{response.text[:200]}"
            ) from exc

        response.raise_for_status()
        return response.status_code, body

    def delete_journal_entry(self, entry_id: str) -> int:
        """Delete a journal entry by ID.

        Returns:
            int: HTTP status code

        Raises:
            requests.exceptions.RequestException: On connection/timeout errors
        """
        url: str = f"{self.base_url}/journal/{entry_id}"

        try:
            response = requests.delete(url, timeout=API_REQUEST_TIMEOUT_SEC)
        except requests.exceptions.RequestException as exc:
            raise requests.exceptions.RequestException(f"Failed to DELETE {url}: {exc}") from exc

        response.raise_for_status()
        return response.status_code
