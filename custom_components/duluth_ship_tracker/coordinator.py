"""Data update coordinator for Duluth Ship Tracker."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HarborLookoutApi, HarborLookoutApiError
from .const import DOMAIN, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


class DuluthShipTrackerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Duluth ship data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: HarborLookoutApi,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            ships = await self.api.get_ships()

            return {
                "raw_ships": ships,
                "arriving": self.api.get_arriving_ships(ships),
                "departing": self.api.get_departing_ships(ships),
                "in_harbor": self.api.get_ships_in_harbor(ships),
                "total_count": len(ships),
            }
        except HarborLookoutApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
