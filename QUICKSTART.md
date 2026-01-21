# Quick Start Guide

Get up and running with Duluth Ship Tracker in 5 minutes!

## TL;DR

```bash
# 1. Copy to Home Assistant
cp -r custom_components/duluth_ship_tracker /config/custom_components/

# 2. Restart Home Assistant
# Settings → System → Restart

# 3. Add Integration
# Settings → Devices & Services → Add Integration → "Duluth Ship Tracker"

# Done! 🎉
```

## What You Get

After installation, you'll have:

✅ **9 sensors** tracking Duluth Harbor ships
✅ **Real-time data** updated every 15 minutes
✅ **Ship details** including name, type, cargo, position
✅ **Ready-to-use automations** for TTS announcements
✅ **15-minute warnings** for arrivals and departures

## Essential Sensors

| Sensor | What it shows |
|--------|--------------|
| `sensor.duluth_arriving_ships` | Count of incoming ships |
| `sensor.duluth_departing_ships` | Count of outgoing ships |
| `sensor.duluth_next_arriving_ship` | Next ship arriving with full details |
| `sensor.duluth_next_departing_ship` | Next ship departing with full details |

## Quick Dashboard Card

Add this to your Lovelace dashboard:

```yaml
type: entities
title: Duluth Harbor
entities:
  - entity: sensor.duluth_arriving_ships
    name: Arriving Today
  - entity: sensor.duluth_departing_ships
    name: Departing Today
  - entity: sensor.duluth_ships_in_harbor
    name: Currently in Harbor
  - entity: sensor.duluth_next_arriving_ship
    name: Next Arrival
  - entity: sensor.duluth_next_departing_ship
    name: Next Departure
```

## Quick TTS Announcement

Want a daily ship schedule announcement? Add this automation:

```yaml
alias: Daily Ship Report
trigger:
  - platform: time
    at: "08:00:00"
action:
  - service: tts.google_translate_say
    data:
      entity_id: media_player.living_room
      message: >
        Good morning! {{ states('sensor.duluth_arriving_ships') }} ships
        arriving and {{ states('sensor.duluth_departing_ships') }} ships
        departing Duluth Harbor today.
```

## Quick 15-Minute Warning

Get notified before ships arrive:

```yaml
alias: Ship Arrival Warning
trigger:
  - platform: time_pattern
    minutes: "/1"
condition:
  - condition: template
    value_template: >
      {% set arrival = state_attr('sensor.duluth_next_arriving_ship', 'arrival_time') %}
      {% if arrival %}
        {% set arrival_time = arrival | as_datetime %}
        {% set minutes = (arrival_time - now()).total_seconds() / 60 %}
        {{ minutes > 14 and minutes <= 16 }}
      {% else %}
        false
      {% endif %}
action:
  - service: notify.notify
    data:
      message: >
        {{ state_attr('sensor.duluth_next_arriving_ship', 'ship_name') }}
        arriving in 15 minutes!
```

## Troubleshooting

### No data showing?
1. Check if Harbor Lookout API is accessible: Visit https://harborlookout.com/
2. Check Home Assistant logs for errors
3. Ships may not be active during winter months

### Sensors not created?
1. Verify files are in `/config/custom_components/duluth_ship_tracker/`
2. Restart Home Assistant
3. Check logs for errors

### TTS not working?
1. Make sure you have a TTS platform configured
2. Update `media_player.living_room` to your actual media player
3. Test TTS manually in Developer Tools

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🔧 See [INSTALL.md](INSTALL.md) for detailed installation
- 🧪 Use [TESTING.md](TESTING.md) to verify everything works
- 📝 Customize automations in `automations.yaml`
- 🎨 Add more dashboard cards

## Get Help

- 🐛 [Report issues](https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant/issues)
- 💬 [Ask questions](https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant/discussions)
- 🏠 [Home Assistant Community](https://community.home-assistant.io/)

---

**Enjoy tracking ships! ⚓🚢**
