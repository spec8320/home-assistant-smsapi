"""Notify entity platform for SMSAPI.pl."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import NotifyEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import SmsApiClient, SmsApiError
from .const import CONF_DEFAULT_RECIPIENTS, CONF_DEFAULT_SENDER, DOMAIN
from .helpers import get_entry_value, prepare_recipients

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the SMSAPI notify entity."""
    runtime = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SmsApiNotifyEntity(entry, runtime["client"])])


class SmsApiNotifyEntity(NotifyEntity):
    """Notify entity sending SMS messages through SMSAPI.pl."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:message-text"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry, client: SmsApiClient) -> None:
        """Initialize the entity."""
        self._entry = entry
        self._client = client
        self._attr_unique_id = entry.entry_id

    async def async_send_message(
        self,
        message: str,
        title: str | None = None,
    ) -> None:
        """Send a message to the configured default recipients."""
        recipients = self._entry.data.get(CONF_DEFAULT_RECIPIENTS, [])
        if not recipients:
            raise HomeAssistantError(
                "Brak domyślnych odbiorców. Skonfiguruj ich w opcjach SMSAPI.pl "
                "albo użyj akcji smsapi.send_sms."
            )

        sender = self._entry.data.get(CONF_DEFAULT_SENDER) or None
        final_message = f"{title}: {message}" if title else message

        try:
            await self._client.async_send_sms(
                recipients=recipients,
                message=final_message,
                sender=sender,
            )
        except SmsApiError as err:
            _LOGGER.error("SMSAPI notify failed: %s", err)
            raise HomeAssistantError(str(err)) from err

        self._async_record_notification()
