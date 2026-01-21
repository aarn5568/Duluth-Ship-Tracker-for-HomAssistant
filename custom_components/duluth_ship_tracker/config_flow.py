"""Config flow for Duluth Ship Tracker integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import HarborLookoutApi, HarborLookoutApiError
from .const import (
    CONF_ANNOUNCEMENT_TIME,
    CONF_TTS_SERVICE,
    CONF_WARNING_MINUTES,
    DEFAULT_ANNOUNCEMENT_TIME,
    DEFAULT_TTS_SERVICE,
    DEFAULT_WARNING_MINUTES,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def validate_api(hass: HomeAssistant) -> bool:
    """Validate the API connection."""
    session = async_get_clientsession(hass)
    api = HarborLookoutApi(session)

    try:
        await api.get_ships()
        return True
    except HarborLookoutApiError as err:
        _LOGGER.error("Failed to connect to Harbor Lookout API: %s", err)
        return False


class DuluthShipTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Duluth Ship Tracker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate API connection
            if await validate_api(self.hass):
                return self.async_create_entry(
                    title="Duluth Ship Tracker",
                    data={},
                    options=user_input,
                )
            errors["base"] = "cannot_connect"

        # Show configuration form
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ANNOUNCEMENT_TIME,
                    default=DEFAULT_ANNOUNCEMENT_TIME,
                ): str,
                vol.Optional(
                    CONF_WARNING_MINUTES,
                    default=DEFAULT_WARNING_MINUTES,
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=120)),
                vol.Optional(
                    CONF_TTS_SERVICE,
                    default=DEFAULT_TTS_SERVICE,
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> DuluthShipTrackerOptionsFlow:
        """Get the options flow for this handler."""
        return DuluthShipTrackerOptionsFlow(config_entry)


class DuluthShipTrackerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Duluth Ship Tracker."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ANNOUNCEMENT_TIME,
                    default=options.get(CONF_ANNOUNCEMENT_TIME, DEFAULT_ANNOUNCEMENT_TIME),
                ): str,
                vol.Optional(
                    CONF_WARNING_MINUTES,
                    default=options.get(CONF_WARNING_MINUTES, DEFAULT_WARNING_MINUTES),
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=120)),
                vol.Optional(
                    CONF_TTS_SERVICE,
                    default=options.get(CONF_TTS_SERVICE, DEFAULT_TTS_SERVICE),
                ): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
