"""Asynchronous client for SMSAPI.pl."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession


@dataclass(slots=True)
class SmsApiError(Exception):
    """Error returned while communicating with SMSAPI."""

    message: str
    status: int | None = None
    response: Any | None = None

    def __str__(self) -> str:
        return self.message


class SmsApiClient:
    """Small async SMSAPI.pl REST client."""

    def __init__(self, session: ClientSession, token: str, api_url: str) -> None:
        self._session = session
        self._token = token
        self._api_url = api_url

    async def async_send_sms(
        self,
        recipients: list[str],
        message: str,
        sender: str | None = None,
        normalize: bool = False,
        fast: bool = False,
    ) -> dict[str, Any]:
        """Send an SMS and return the decoded SMSAPI response."""
        payload: dict[str, str] = {
            "to": ",".join(recipients),
            "message": message,
            "format": "json",
            "encoding": "utf-8",
        }

        if sender:
            payload["from"] = sender
        if normalize:
            payload["normalize"] = "1"
        if fast:
            payload["fast"] = "1"

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }

        try:
            async with self._session.post(
                self._api_url,
                data=payload,
                headers=headers,
                timeout=30,
            ) as response:
                try:
                    body: Any = await response.json(content_type=None)
                except ValueError:
                    body = await response.text()

                if response.status >= 400:
                    raise SmsApiError(
                        self._extract_error(body, response.status),
                        status=response.status,
                        response=body,
                    )

                if isinstance(body, dict) and body.get("error"):
                    raise SmsApiError(
                        self._extract_error(body, response.status),
                        status=response.status,
                        response=body,
                    )

                return body if isinstance(body, dict) else {"response": body}

        except SmsApiError:
            raise
        except (ClientError, TimeoutError) as err:
            raise SmsApiError(f"Nie udało się połączyć z SMSAPI: {err}") from err

    @staticmethod
    def _extract_error(body: Any, status: int) -> str:
        if isinstance(body, dict):
            code = body.get("error")
            message = body.get("message") or body.get("error_message")
            if code and message:
                return f"SMSAPI zwróciło błąd {code}: {message}"
            if message:
                return f"SMSAPI zwróciło błąd: {message}"
            if code:
                return f"SMSAPI zwróciło błąd {code}"
        if isinstance(body, str) and body.strip():
            return f"SMSAPI zwróciło HTTP {status}: {body.strip()}"
        return f"SMSAPI zwróciło HTTP {status}"
