from typing import Any

import httpx


class LogSentinelClient:
    """
    A simple HTTP client for interacting with the LogSentinel API.
    """

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def send_log(self, parser_type: str, raw_log: str) -> dict[str, Any] | None:
        """
        Sends a single log line to the API.
        """
        url = f"{self.base_url}/parse/{parser_type}"
        payload = {"raw_log": raw_log}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Error sending log to {url}: {e}")
            return None

    def send_batch(self, parser_type: str, raw_logs: list[str]) -> list[dict[str, Any]] | None:
        """
        Sends a batch of log lines to the API.
        """
        url = f"{self.base_url}/parse/{parser_type}/batch"
        payload = {"raw_logs": raw_logs}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Error sending batch to {url}: {e}")
            return None
