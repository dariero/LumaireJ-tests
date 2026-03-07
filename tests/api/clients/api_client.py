"""Simple API client for endpoints."""

import json
from typing import Any

import requests

from tests.shared.constants import API_REQUEST_TIMEOUT_SEC


class APIClient:
    """Simple client for API endpoints."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Send an HTTP request; raises RequestException on connection/timeout errors."""
        url = f"{self.base_url}{path}"
        try:
            return requests.request(method, url, timeout=API_REQUEST_TIMEOUT_SEC, **kwargs)
        except requests.exceptions.RequestException as exc:
            raise requests.exceptions.RequestException(
                f"Failed to {method} {url}: {exc}"
            ) from exc

    def create_journal_entry(self, content: str, mood: str = "") -> tuple[int, dict[str, Any]]:
        """Create a new journal entry.

        Returns:
            tuple: (status_code, response_body)

        Raises:
            requests.exceptions.HTTPError: On non-2xx response.
            requests.exceptions.RequestException: On connection/timeout errors.
            ValueError: On non-JSON response body.
        """
        payload: dict[str, str] = {"content": content}
        if mood:
            payload["mood"] = mood

        response = self._request("POST", "/journal", json=payload)
        response.raise_for_status()

        try:
            body = response.json()
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Non-JSON response from POST /journal (status {response.status_code}): "
                f"{response.text[:200]}"
            ) from exc

        return response.status_code, body

    def delete_journal_entry(self, entry_id: str) -> int:
        """Delete a journal entry by ID.

        Returns:
            int: HTTP status code

        Raises:
            requests.exceptions.HTTPError: On non-2xx response.
            requests.exceptions.RequestException: On connection/timeout errors.
        """
        response = self._request("DELETE", f"/journal/{entry_id}")
        response.raise_for_status()
        return response.status_code
