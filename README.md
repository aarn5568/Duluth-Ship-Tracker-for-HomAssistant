# Duluth Ship Tracker for Home Assistant

A Home Assistant custom component that tracks ships entering and leaving Duluth Harbor using data from Harbor Lookout. Features daily TTS announcements, 15-minute arrival/departure warnings, and detailed ship information.

## Features

- 📊 **Real-time Ship Tracking**: Monitor all ships in Duluth Harbor
- 🔔 **Daily Announcements**: TTS announcements of the day's ship schedule
- ⏰ **15-Minute Warnings**: Advance notifications before arrivals/departures
- 🚢 **Detailed Ship Info**: Name, type, cargo, destination, and more
- 📍 **Live Positioning**: Real-time coordinates, speed, and heading
- 🎯 **Multiple Sensors**: Separate tracking for arriving, departing, and docked ships

## Installation

### Method 1: Manual Installation

1. Copy the `custom_components/duluth_ship_tracker` folder to your Home Assistant's `config/custom_components/` directory:

```bash
# If using SSH/SCP
scp -r custom_components/duluth_ship_tracker/ user@homeassistant:/config/custom_components/

# Or using Samba/File Share
# Copy the folder to: \\homeassistant\config\custom_components\
```

2. Your directory structure should look like:
```
/config/
├── custom_components/
│   └── duluth_ship_tracker/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── api.py
│       ├── coordinator.py
│       ├── sensor.py
│       └── strings.json
└── configuration.yaml
```

3. Restart Home Assistant

4. Add the integration:
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for "**Duluth Ship Tracker**"
   - Click to add and configure

### Method 2: HACS (Future)

_This integration will be submitted to HACS for easier installation._

## Configuration

During setup, you can configure:

- **Daily Announcement Time**: Time for daily ship schedule announcement (default: 08:00)
- **Warning Minutes**: How many minutes before arrival/departure to notify (default: 15)
- **TTS Service**: Which text-to-speech service to use (default: tts.google_translate_say)

These settings can be changed later via **Settings** → **Devices & Services** → **Duluth Ship Tracker** → **Configure**.

## Sensors Created

The integration creates the following sensors:

### Count Sensors
- `sensor.duluth_arriving_ships` - Number of ships arriving
- `sensor.duluth_departing_ships` - Number of ships departing
- `sensor.duluth_ships_in_harbor` - Number of ships currently in harbor
- `sensor.duluth_total_ships` - Total number of tracked ships

### Next Ship Sensors
- `sensor.duluth_next_arriving_ship` - Next ship arriving (with full details)
- `sensor.duluth_next_departing_ship` - Next ship departing (with full details)

### List Sensors
- `sensor.duluth_arriving_ships_list` - Complete list of arriving ships
- `sensor.duluth_departing_ships_list` - Complete list of departing ships
- `sensor.duluth_ships_in_harbor_list` - Complete list of ships in harbor

## Sensor Attributes

Each ship sensor includes detailed attributes:

- `ship_name` - Name of the vessel
- `ship_type` - Type of vessel (cargo, tanker, etc.)
- `cargo` - Current cargo information
- `destination` - Destination port
- `arrival_time` / `departure_time` - Scheduled times
- `latitude` / `longitude` - Current position
- `speed` - Current speed
- `heading` - Current heading/course
- `nationality` - Flag/country of registration
- `status` - Current status (moored, anchored, underway, etc.)

## Automations

### Daily Schedule Announcement

Copy the example automations from `automations.yaml` to your Home Assistant automations, or create them via the UI.

**Example**: Daily announcement at 8 AM
```yaml
- id: duluth_daily_ship_announcement
  alias: "Duluth Daily Ship Announcement"
  trigger:
    - platform: time
      at: "08:00:00"
  condition:
    - condition: or
      conditions:
        - condition: numeric_state
          entity_id: sensor.duluth_arriving_ships
          above: 0
        - condition: numeric_state
          entity_id: sensor.duluth_departing_ships
          above: 0
  action:
    - service: tts.google_translate_say
      data:
        entity_id: media_player.home
        message: >
          Good morning. Today's Duluth Harbor schedule:
          {{ states('sensor.duluth_arriving_ships') }} ships arriving,
          {{ states('sensor.duluth_departing_ships') }} ships departing.
```

### 15-Minute Warnings

**Example**: Arrival warning
```yaml
- id: duluth_ship_arrival_warning
  alias: "Duluth Ship Arrival Warning"
  trigger:
    - platform: time_pattern
      minutes: "/1"
  condition:
    - condition: template
      value_template: >
        {% set arrival = state_attr('sensor.duluth_next_arriving_ship', 'arrival_time') %}
        {% if arrival %}
          {% set arrival_time = arrival | as_datetime %}
          {% set time_until = (arrival_time - now()).total_seconds() / 60 %}
          {{ time_until > 14 and time_until <= 16 }}
        {% else %}
          false
        {% endif %}
  action:
    - service: tts.google_translate_say
      data:
        entity_id: media_player.home
        message: >
          {{ state_attr('sensor.duluth_next_arriving_ship', 'ship_name') }}
          will arrive in approximately 15 minutes.
```

## Lovelace Dashboard Examples

### Simple Card
```yaml
type: entities
title: Duluth Harbor Ships
entities:
  - sensor.duluth_arriving_ships
  - sensor.duluth_departing_ships
  - sensor.duluth_ships_in_harbor
  - sensor.duluth_next_arriving_ship
  - sensor.duluth_next_departing_ship
```

### Detailed Ship Card
```yaml
type: markdown
title: Next Arriving Ship
content: >
  **{{ state_attr('sensor.duluth_next_arriving_ship', 'ship_name') }}**

  - **Type**: {{ state_attr('sensor.duluth_next_arriving_ship', 'ship_type') }}
  - **Cargo**: {{ state_attr('sensor.duluth_next_arriving_ship', 'cargo') }}
  - **ETA**: {{ state_attr('sensor.duluth_next_arriving_ship', 'arrival_time') }}
  - **Nationality**: {{ state_attr('sensor.duluth_next_arriving_ship', 'nationality') }}
```

### Map Card (Shows ship positions)
```yaml
type: map
entities:
  - sensor.duluth_next_arriving_ship
default_zoom: 12
```

## Future Development

Planned features for future releases:

- 🖼️ **Interactive Ship App**: Click on ships to learn more
- 📦 **Cargo Details**: Expanded cargo information
- 📊 **Historical Data**: Track ship visit history
- 🗺️ **Route Tracking**: Show ship routes and paths
- 📷 **Harbor Cam Integration**: Link to live harbor cameras
- 🔗 **Harbor Lookout Integration**: Deep links to ship details

## Data Source

This integration uses the Harbor Lookout API:
- Website: https://harborlookout.com/
- API updates every 15 minutes
- Real-time AIS data from Duluth-Superior Harbor

## Troubleshooting

### Integration won't load
1. Check Home Assistant logs: **Settings** → **System** → **Logs**
2. Ensure all files are in the correct directory
3. Verify file permissions (should be readable by Home Assistant)
4. Restart Home Assistant after installation

### No data showing
1. Check your internet connection
2. Verify the Harbor Lookout API is accessible
3. Look for errors in the logs
4. Try reloading the integration

### TTS not working
1. Verify your TTS service is configured in Home Assistant
2. Check the TTS entity ID in the integration options
3. Test TTS manually: **Developer Tools** → **Services** → TTS service

## Support

- **Issues**: https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant/issues
- **Discussions**: https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant/discussions

## Credits

- Data provided by [Harbor Lookout](https://harborlookout.com/)
- Inspired by ship watchers of Duluth, Minnesota

## License

MIT License - See LICENSE file for details