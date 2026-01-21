"""Constants for the Duluth Ship Tracker integration."""

DOMAIN = "duluth_ship_tracker"

# API Configuration
API_URL = "https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay"
API_TIMEOUT = 30

# Update intervals
UPDATE_INTERVAL_MINUTES = 15
ANNOUNCEMENT_CHECK_INTERVAL_MINUTES = 1

# Configuration keys
CONF_ANNOUNCEMENT_TIME = "announcement_time"
CONF_WARNING_MINUTES = "warning_minutes"
CONF_TTS_SERVICE = "tts_service"

# Default values
DEFAULT_ANNOUNCEMENT_TIME = "08:00"
DEFAULT_WARNING_MINUTES = 15
DEFAULT_TTS_SERVICE = "tts.google_translate_say"

# Attributes
ATTR_SHIP_NAME = "ship_name"
ATTR_ARRIVAL_TIME = "arrival_time"
ATTR_DEPARTURE_TIME = "departure_time"
ATTR_CARGO = "cargo"
ATTR_DESTINATION = "destination"
ATTR_SHIP_TYPE = "ship_type"
ATTR_LENGTH = "length"
ATTR_WIDTH = "width"
ATTR_NATIONALITY = "nationality"
ATTR_STATUS = "status"
ATTR_DIRECTION = "direction"
ATTR_SPEED = "speed"
ATTR_HEADING = "heading"
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"
ATTR_LAST_UPDATE = "last_update"

# Event types
EVENT_SHIP_ARRIVING = "duluth_ship_tracker_ship_arriving"
EVENT_SHIP_DEPARTING = "duluth_ship_tracker_ship_departing"
EVENT_DAILY_ANNOUNCEMENT = "duluth_ship_tracker_daily_announcement"
