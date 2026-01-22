"""Sensor platform for Duluth Ship Tracker."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_ARRIVAL_TIME,
    ATTR_CARGO,
    ATTR_DEPARTURE_TIME,
    ATTR_DESTINATION,
    ATTR_HEADING,
    ATTR_LAST_UPDATE,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_NATIONALITY,
    ATTR_SHIP_NAME,
    ATTR_SHIP_TYPE,
    ATTR_SPEED,
    ATTR_STATUS,
    DOMAIN,
)
from .coordinator import DuluthShipTrackerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Duluth Ship Tracker sensors."""
    coordinator: DuluthShipTrackerCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        DuluthShipCountSensor(coordinator, "arriving", "Arriving Ships"),
        DuluthShipCountSensor(coordinator, "departing", "Departing Ships"),
        DuluthShipCountSensor(coordinator, "in_harbor", "Ships in Harbor"),
        DuluthShipCountSensor(coordinator, "total_count", "Total Ships"),
        DuluthNextArrivalSensor(coordinator),
        DuluthNextDepartureSensor(coordinator),
        DuluthShipListSensor(coordinator, "arriving", "Arriving Ships List"),
        DuluthShipListSensor(coordinator, "departing", "Departing Ships List"),
        DuluthShipListSensor(coordinator, "in_harbor", "Ships in Harbor List"),
    ]

    async_add_entities(entities)


class DuluthShipCountSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing count of ships."""

    def __init__(
        self,
        coordinator: DuluthShipTrackerCoordinator,
        data_key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Duluth {name}"
        self._attr_unique_id = f"{DOMAIN}_{data_key}_count"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "ships"
        self._attr_icon = "mdi:ferry"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self._data_key == "total_count":
            return self.coordinator.data.get(self._data_key, 0)
        return len(self.coordinator.data.get(self._data_key, []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "last_update": datetime.now().isoformat(),
        }


class DuluthNextArrivalSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing next arriving ship."""

    def __init__(self, coordinator: DuluthShipTrackerCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Duluth Next Arriving Ship"
        self._attr_unique_id = f"{DOMAIN}_next_arrival"
        self._attr_icon = "mdi:ferry"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        arriving = self.coordinator.data.get("arriving", [])
        if not arriving:
            return "No arrivals scheduled"

        next_ship = arriving[0]
        return next_ship.get("ship_name", "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        arriving = self.coordinator.data.get("arriving", [])
        if not arriving:
            return {}

        next_ship = arriving[0]
        arrival_time = next_ship.get("arrival_time") or next_ship.get("eta")

        attrs = {
            ATTR_SHIP_NAME: next_ship.get("ship_name"),
            ATTR_CARGO: next_ship.get("cargo"),
            ATTR_DESTINATION: next_ship.get("destination"),
            ATTR_SHIP_TYPE: next_ship.get("ship_type"),
            ATTR_NATIONALITY: next_ship.get("nationality"),
            ATTR_STATUS: next_ship.get("status"),
        }

        if arrival_time:
            attrs[ATTR_ARRIVAL_TIME] = arrival_time.isoformat() if isinstance(arrival_time, datetime) else arrival_time

        if next_ship.get("latitude") and next_ship.get("longitude"):
            attrs[ATTR_LATITUDE] = next_ship.get("latitude")
            attrs[ATTR_LONGITUDE] = next_ship.get("longitude")
            attrs[ATTR_SPEED] = next_ship.get("speed")
            attrs[ATTR_HEADING] = next_ship.get("heading")

        return {k: v for k, v in attrs.items() if v is not None}


class DuluthNextDepartureSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing next departing ship."""

    def __init__(self, coordinator: DuluthShipTrackerCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Duluth Next Departing Ship"
        self._attr_unique_id = f"{DOMAIN}_next_departure"
        self._attr_icon = "mdi:ferry"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        departing = self.coordinator.data.get("departing", [])
        if not departing:
            return "No departures scheduled"

        next_ship = departing[0]
        return next_ship.get("ship_name", "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        departing = self.coordinator.data.get("departing", [])
        if not departing:
            return {}

        next_ship = departing[0]
        departure_time = next_ship.get("departure_time") or next_ship.get("etd")

        attrs = {
            ATTR_SHIP_NAME: next_ship.get("ship_name"),
            ATTR_CARGO: next_ship.get("cargo"),
            ATTR_DESTINATION: next_ship.get("destination"),
            ATTR_SHIP_TYPE: next_ship.get("ship_type"),
            ATTR_NATIONALITY: next_ship.get("nationality"),
            ATTR_STATUS: next_ship.get("status"),
        }

        if departure_time:
            attrs[ATTR_DEPARTURE_TIME] = departure_time.isoformat() if isinstance(departure_time, datetime) else departure_time

        if next_ship.get("latitude") and next_ship.get("longitude"):
            attrs[ATTR_LATITUDE] = next_ship.get("latitude")
            attrs[ATTR_LONGITUDE] = next_ship.get("longitude")
            attrs[ATTR_SPEED] = next_ship.get("speed")
            attrs[ATTR_HEADING] = next_ship.get("heading")

        return {k: v for k, v in attrs.items() if v is not None}


class DuluthShipListSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing list of ships."""

    def __init__(
        self,
        coordinator: DuluthShipTrackerCoordinator,
        data_key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"Duluth {name}"
        self._attr_unique_id = f"{DOMAIN}_{data_key}_list"
        self._attr_icon = "mdi:format-list-bulleted"

    @property
    def native_value(self) -> int:
        """Return the count."""
        return len(self.coordinator.data.get(self._data_key, []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return ship list as attributes."""
        ships = self.coordinator.data.get(self._data_key, [])

        ship_list = []
        for ship in ships:
            ship_info = {
                "name": ship.get("ship_name", "Unknown"),
                "type": ship.get("ship_type"),
                "cargo": ship.get("cargo"),
                "destination": ship.get("destination"),
                "status": ship.get("status"),
            }

            # Add timing information
            if self._data_key == "arriving":
                arrival = ship.get("arrival_time") or ship.get("eta")
                if arrival:
                    ship_info["arrival_time"] = arrival.isoformat() if isinstance(arrival, datetime) else arrival
            elif self._data_key == "departing":
                departure = ship.get("departure_time") or ship.get("etd")
                if departure:
                    ship_info["departure_time"] = departure.isoformat() if isinstance(departure, datetime) else departure

            # Clean up None values
            ship_info = {k: v for k, v in ship_info.items() if v is not None}
            ship_list.append(ship_info)

        return {
            "ships": ship_list,
            "count": len(ship_list),
            ATTR_LAST_UPDATE: datetime.now().isoformat(),
        }
