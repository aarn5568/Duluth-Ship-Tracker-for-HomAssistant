"""API client for Harbor Lookout."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

import aiohttp
import async_timeout

from .const import API_TIMEOUT, API_URL

_LOGGER = logging.getLogger(__name__)


class HarborLookoutApiError(Exception):
    """Exception raised for API errors."""


class HarborLookoutApi:
    """API client for Harbor Lookout."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self.session = session
        self._last_data: list[dict[str, Any]] = []

    async def get_ships(self) -> list[dict[str, Any]]:
        """Fetch ship data from Harbor Lookout API."""
        try:
            async with async_timeout.timeout(API_TIMEOUT):
                async with self.session.get(API_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if not isinstance(data, list):
                        _LOGGER.error("Unexpected API response format: %s", type(data))
                        return self._last_data

                    self._last_data = data
                    _LOGGER.debug("Fetched %d ships from API", len(data))
                    return data

        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout fetching ship data: %s", err)
            raise HarborLookoutApiError("API request timed out") from err
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching ship data: %s", err)
            raise HarborLookoutApiError(f"API request failed: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error fetching ship data: %s", err)
            raise HarborLookoutApiError(f"Unexpected error: {err}") from err

    def parse_ship_data(self, ship: dict[str, Any]) -> dict[str, Any]:
        """Parse raw ship data into structured format."""
        # The actual field names will need to be adjusted based on the API response
        # This is a template based on typical ship tracking data
        return {
            "ship_name": ship.get("name", "Unknown"),
            "mmsi": ship.get("mmsi"),
            "imo": ship.get("imo"),
            "ship_type": ship.get("type", "Unknown"),
            "status": ship.get("status", "Unknown"),
            "cargo": ship.get("cargo", "Unknown"),
            "destination": ship.get("destination"),
            "eta": self._parse_timestamp(ship.get("eta")),
            "etd": self._parse_timestamp(ship.get("etd")),
            "arrival_time": self._parse_timestamp(ship.get("arrivalTime")),
            "departure_time": self._parse_timestamp(ship.get("departureTime")),
            "latitude": ship.get("latitude") or ship.get("lat"),
            "longitude": ship.get("longitude") or ship.get("lon") or ship.get("lng"),
            "speed": ship.get("speed"),
            "heading": ship.get("heading") or ship.get("course"),
            "length": ship.get("length"),
            "width": ship.get("width") or ship.get("beam"),
            "nationality": ship.get("nationality") or ship.get("flag"),
            "last_update": self._parse_timestamp(ship.get("lastUpdate") or ship.get("timestamp")),
        }

    def _parse_timestamp(self, timestamp: Any) -> datetime | None:
        """Parse various timestamp formats."""
        if not timestamp:
            return None

        if isinstance(timestamp, datetime):
            return timestamp

        if isinstance(timestamp, (int, float)):
            # Unix timestamp
            return datetime.fromtimestamp(timestamp)

        if isinstance(timestamp, str):
            # Try common ISO formats
            for fmt in [
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
            ]:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue

        return None

    def get_arriving_ships(self, ships: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter ships that are arriving."""
        arriving = []
        for ship in ships:
            parsed = self.parse_ship_data(ship)
            arrival_time = parsed.get("arrival_time") or parsed.get("eta")
            if arrival_time and arrival_time > datetime.now():
                arriving.append(parsed)

        # Sort by arrival time
        arriving.sort(key=lambda x: x.get("arrival_time") or x.get("eta") or datetime.max)
        return arriving

    def get_departing_ships(self, ships: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter ships that are departing."""
        departing = []
        for ship in ships:
            parsed = self.parse_ship_data(ship)
            departure_time = parsed.get("departure_time") or parsed.get("etd")
            if departure_time and departure_time > datetime.now():
                departing.append(parsed)

        # Sort by departure time
        departing.sort(key=lambda x: x.get("departure_time") or x.get("etd") or datetime.max)
        return departing

    def get_ships_in_harbor(self, ships: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter ships currently in harbor."""
        in_harbor = []
        for ship in ships:
            parsed = self.parse_ship_data(ship)
            status = parsed.get("status", "").lower()
            # Adjust status checks based on actual API values
            if status in ["moored", "anchored", "at berth", "docked"]:
                in_harbor.append(parsed)

        return in_harbor
