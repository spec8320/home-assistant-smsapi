"""Shared helpers for the SMSAPI.pl integration."""

from __future__ import annotations

import re
from typing import Any

from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_DEFAULT_RECIPIENTS,
    CONF_DEFAULT_SENDER,
    CONF_TOKEN,
)

PHONE_RE = re.compile(r"^\+?[1-9]\d{7,14}$")


def get_entry_value(entry: ConfigEntry, key: str, default: Any = None) -> Any:
    """Return an option value, falling back to entry data."""
    if key in entry.options:
        return entry.options[key]
    return entry.data.get(key, default)


def normalize_phone_number(number: str) -> str:
    """Remove common separators while preserving an optional leading plus."""
    return (
        str(number)
        .strip()
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def prepare_recipients(raw_recipients: list[str]) -> list[str]:
    """Normalize a list of phone numbers."""
    return [normalize_phone_number(number) for number in raw_recipients]


def entry_settings(entry: ConfigEntry) -> dict[str, Any]:
    """Return effective integration settings."""
    return {
        CONF_TOKEN: get_entry_value(entry, CONF_TOKEN, ""),
        CONF_DEFAULT_SENDER: get_entry_value(
            entry, CONF_DEFAULT_SENDER, ""
        ),
        CONF_DEFAULT_RECIPIENTS: get_entry_value(
            entry, CONF_DEFAULT_RECIPIENTS, []
        ),
    }
