"""SMSAPI.pl integration for Home Assistant."""

from __future__ import annotations

import logging
from functools import partial
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.notify import ATTR_MESSAGE
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmsApiClient, SmsApiError
from .helpers import PHONE_RE, get_entry_value, prepare_recipients
from .const import (
    API_URL,
    CONF_DEFAULT_RECIPIENTS,
    CONF_DEFAULT_SENDER,
    CONF_TOKEN,
    DOMAIN,
    SERVICE_SEND_SMS,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


SERVICE_SCHEMA = vol.Schema(
    {
        vol.Optional("recipients"): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional("sender"): cv.string,
        vol.Optional("normalize", default=False): cv.boolean,
        vol.Optional("fast", default=False): cv.boolean,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SMSAPI.pl from a config entry."""
    token = get_entry_value(entry, CONF_TOKEN, "")
    client = SmsApiClient(async_get_clientsession(hass), token, API_URL)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "entry": entry,
    }

    if not hass.services.has_service(DOMAIN, SERVICE_SEND_SMS):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SEND_SMS,
            partial(_async_handle_send_sms, hass),
            schema=SERVICE_SCHEMA,
            supports_response=SupportsResponse.OPTIONAL,
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload SMSAPI.pl config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)

    if not hass.data.get(DOMAIN):
        hass.services.async_remove(DOMAIN, SERVICE_SEND_SMS)
        hass.data.pop(DOMAIN, None)

    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration after reconfiguration."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_handle_send_sms(
    hass: HomeAssistant, call: ServiceCall
) -> ServiceResponse:
    """Handle smsapi.send_sms."""
    integrations: dict[str, dict[str, Any]] = hass.data.get(DOMAIN, {})

    if not integrations:
        raise HomeAssistantError("Integracja SMSAPI.pl nie jest skonfigurowana")

    runtime = next(iter(integrations.values()))
    entry: ConfigEntry = runtime["entry"]
    client: SmsApiClient = runtime["client"]

    recipients = call.data.get("recipients") or get_entry_value(
        entry, CONF_DEFAULT_RECIPIENTS, []
    )
    recipients = prepare_recipients(recipients)

    if not recipients:
        raise ServiceValidationError(
            "Podaj recipients albo ustaw domyślnych odbiorców w konfiguracji integracji"
        )

    invalid = [number for number in recipients if not PHONE_RE.fullmatch(number)]
    if invalid:
        raise ServiceValidationError(
            "Niepoprawny numer telefonu: " + ", ".join(invalid)
        )

    sender = call.data.get("sender")
    if sender is None:
        sender = get_entry_value(entry, CONF_DEFAULT_SENDER, "") or None

    if sender and len(sender) > 11:
        raise ServiceValidationError("Pole nadawcy może mieć maksymalnie 11 znaków")

    message = call.data[ATTR_MESSAGE].strip()
    if not message:
        raise ServiceValidationError("Treść wiadomości nie może być pusta")

    try:
        result = await client.async_send_sms(
            recipients=recipients,
            message=message,
            sender=sender,
            normalize=call.data["normalize"],
            fast=call.data["fast"],
        )
    except SmsApiError as err:
        _LOGGER.error("SMSAPI send failed: %s; response=%s", err, err.response)
        raise HomeAssistantError(str(err)) from err

    _LOGGER.info("SMSAPI accepted SMS for %s", ", ".join(recipients))
    return result

