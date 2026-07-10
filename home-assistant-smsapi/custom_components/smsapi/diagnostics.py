"""Diagnostics support for SMSAPI.pl."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.redact import async_redact_data

from .const import (
    CONF_DEFAULT_RECIPIENTS,
    CONF_DEFAULT_SENDER,
    CONF_TOKEN,
)
from .helpers import entry_settings

TO_REDACT = {
    CONF_TOKEN,
    CONF_DEFAULT_RECIPIENTS,
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return safe diagnostics for a config entry."""
    settings = entry_settings(entry)

    return {
        "entry": {
            "title": entry.title,
            "version": entry.version,
            "minor_version": entry.minor_version,
            "state": entry.state.value,
        },
        "configuration": async_redact_data(settings, TO_REDACT),
        "summary": {
            "sender_configured": bool(
                settings.get(CONF_DEFAULT_SENDER)
            ),
            "recipient_count": len(
                settings.get(CONF_DEFAULT_RECIPIENTS, [])
            ),
            "token_configured": bool(settings.get(CONF_TOKEN)),
        },
    }
