"""Config and options flows for SMSAPI.pl."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEFAULT_RECIPIENTS,
    CONF_DEFAULT_SENDER,
    CONF_TOKEN,
    DOMAIN,
)
from .helpers import entry_settings


class SmsApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SMSAPI.pl."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SmsApiOptionsFlow:
        """Return the options flow handler."""
        return SmsApiOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle initial setup."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            data = _prepare_data(user_input)
            return self.async_create_entry(title="SMSAPI.pl", data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(),
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Allow changing all connection settings."""
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            data = _prepare_data(user_input)
            return self.async_update_reload_and_abort(
                entry,
                data=data,
                options={},
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(_form_defaults(entry_settings(entry))),
        )


class SmsApiOptionsFlow(config_entries.OptionsFlow):
    """Handle editable SMSAPI.pl options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage SMSAPI.pl options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=_prepare_data(user_input),
            )

        return self.async_show_form(
            step_id="init",
            data_schema=_schema(
                _form_defaults(entry_settings(self.config_entry))
            ),
        )


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    """Build the setup/options schema."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_TOKEN,
                default=defaults.get(CONF_TOKEN, ""),
            ): str,
            vol.Optional(
                CONF_DEFAULT_SENDER,
                default=defaults.get(CONF_DEFAULT_SENDER, ""),
            ): str,
            vol.Optional(
                CONF_DEFAULT_RECIPIENTS,
                default=defaults.get(CONF_DEFAULT_RECIPIENTS, ""),
            ): str,
        }
    )


def _prepare_data(user_input: dict[str, Any]) -> dict[str, Any]:
    """Normalize values entered in a form."""
    recipients = [
        number.strip()
        for number in user_input.get(CONF_DEFAULT_RECIPIENTS, "").split(",")
        if number.strip()
    ]

    return {
        CONF_TOKEN: user_input[CONF_TOKEN].strip(),
        CONF_DEFAULT_SENDER: user_input.get(
            CONF_DEFAULT_SENDER, ""
        ).strip(),
        CONF_DEFAULT_RECIPIENTS: recipients,
    }


def _form_defaults(settings: dict[str, Any]) -> dict[str, Any]:
    """Convert stored values into form defaults."""
    return {
        CONF_TOKEN: settings.get(CONF_TOKEN, ""),
        CONF_DEFAULT_SENDER: settings.get(CONF_DEFAULT_SENDER, ""),
        CONF_DEFAULT_RECIPIENTS: ", ".join(
            settings.get(CONF_DEFAULT_RECIPIENTS, [])
        ),
    }
