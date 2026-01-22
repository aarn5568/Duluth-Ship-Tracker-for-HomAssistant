# Testing Guide for Duluth Ship Tracker

This guide will help you test the integration and verify it's working correctly.

## Pre-Installation API Test

Before installing in Home Assistant, you can verify the API is accessible from your network:

### Option 1: Browser Test
1. Open your browser
2. Navigate to: `https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay`
3. You should see JSON data with ship information

### Option 2: Command Line Test
```bash
curl "https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay"
```

### Option 3: Python Test Script
Run the included test script:
```bash
python3 test_api.py
```

## Post-Installation Testing

Once installed in Home Assistant, follow these steps to verify everything is working:

### Step 1: Check Integration Setup
1. Go to **Settings** → **Devices & Services**
2. Find "Duluth Ship Tracker" in the list
3. Verify status shows "Loaded" (not "Failed" or "Setup failed")

### Step 2: Check Sensor Creation
1. Go to **Developer Tools** → **States**
2. Search for `sensor.duluth`
3. Verify you see these sensors:
   - `sensor.duluth_arriving_ships`
   - `sensor.duluth_departing_ships`
   - `sensor.duluth_ships_in_harbor`
   - `sensor.duluth_total_ships`
   - `sensor.duluth_next_arriving_ship`
   - `sensor.duluth_next_departing_ship`
   - `sensor.duluth_arriving_ships_list`
   - `sensor.duluth_departing_ships_list`
   - `sensor.duluth_ships_in_harbor_list`

### Step 3: Verify Data is Updating
1. Click on any sensor (e.g., `sensor.duluth_total_ships`)
2. Check the state value (should be a number, not "unavailable" or "unknown")
3. Look at "Last Updated" timestamp - should be recent
4. Expand "Attributes" section to see additional data

### Step 4: Test Sensor Attributes
For the "Next Arriving Ship" sensor:
1. Go to **Developer Tools** → **States**
2. Find `sensor.duluth_next_arriving_ship`
3. Expand attributes and verify you see:
   - `ship_name`
   - `ship_type`
   - `cargo`
   - `arrival_time`
   - Other ship details

### Step 5: Check Logs
1. Go to **Settings** → **System** → **Logs**
2. Search for "duluth"
3. Look for any errors or warnings
4. Successful logs should show:
   - "Fetched X ships from API"
   - No error messages about connectivity

### Step 6: Test Manual Refresh
1. Go to **Developer Tools** → **Services**
2. Service: `homeassistant.update_entity`
3. Target: `sensor.duluth_total_ships`
4. Call service
5. Check if sensor updates (timestamp changes)

## Testing Automations

### Test Daily Announcement (Manual)
1. Go to **Developer Tools** → **Services**
2. Service: `script.duluth_announce_daily_schedule`
3. Call service
4. Listen for TTS announcement on your media player

### Test 15-Minute Warning (Simulation)
Since you can't wait for actual ships, test the template logic:

1. Go to **Developer Tools** → **Template**
2. Paste this template:
```jinja
{% set arrival = state_attr('sensor.duluth_next_arriving_ship', 'arrival_time') %}
{% if arrival %}
  {% set arrival_time = arrival | as_datetime %}
  {% set time_until = (arrival_time - now()).total_seconds() / 60 %}
  Time until arrival: {{ time_until | round(1) }} minutes
  Should notify: {{ time_until > 14 and time_until <= 16 }}
{% else %}
  No arrival time available
{% endif %}
```
3. Check the output - this shows the logic used for warnings

## Troubleshooting Tests

### Test 1: Can't Connect to API
**Symptoms**: Sensors show "unavailable", logs show connection errors

**Test**:
```bash
# From your Home Assistant host:
curl -v "https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay"
```

**Possible causes**:
- Firewall blocking outbound HTTPS
- DNS resolution issues
- API endpoint temporarily down

### Test 2: Sensors Not Updating
**Symptoms**: Sensors exist but never change values

**Check**:
1. Integration reload: **Settings** → **Devices & Services** → Duluth Ship Tracker → **⋮** → **Reload**
2. Check update interval: Should update every 15 minutes
3. Check logs for errors during update

### Test 3: No Data in Sensors
**Symptoms**: Sensors show "0" or "No arrivals scheduled"

**This may be normal!** Check:
1. Is there actually ship activity in Duluth Harbor today?
2. Visit https://harborlookout.com/ to verify ships are showing
3. Ships may only be present during shipping season (typically March-January)

### Test 4: TTS Not Working
**Test TTS directly**:
1. **Developer Tools** → **Services**
2. Service: `tts.google_translate_say`
3. Data:
```yaml
entity_id: media_player.home
message: "This is a test"
```
4. Call service - you should hear the message

If this fails, TTS isn't configured properly (not an issue with this integration)

## Expected Data Examples

When working correctly, you should see data like this:

### sensor.duluth_total_ships
```
State: 12
Attributes:
  last_update: 2026-01-21T14:30:00
```

### sensor.duluth_next_arriving_ship
```
State: Paul R. Tregurtha
Attributes:
  ship_name: Paul R. Tregurtha
  ship_type: Bulk Carrier
  cargo: Iron Ore
  arrival_time: 2026-01-21T16:45:00
  destination: Duluth
  nationality: United States
  latitude: 46.7867
  longitude: -92.0842
  speed: 12.3
  heading: 245
```

### sensor.duluth_arriving_ships_list
```
State: 3
Attributes:
  ships:
    - name: Paul R. Tregurtha
      type: Bulk Carrier
      cargo: Iron Ore
      arrival_time: 2026-01-21T16:45:00
    - name: James R. Barker
      type: Bulk Carrier
      cargo: Coal
      arrival_time: 2026-01-21T18:30:00
    - name: American Integrity
      type: Bulk Carrier
      cargo: Taconite
      arrival_time: 2026-01-22T09:15:00
  count: 3
```

## Performance Testing

### Check API Response Time
```bash
time curl "https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay" > /dev/null
```
Should complete in < 5 seconds

### Check Home Assistant Load
1. **Settings** → **System** → **System Health**
2. Note CPU/memory usage
3. Integration should add minimal overhead (< 1% CPU, < 50MB RAM)

## Integration Health Checklist

✅ **Healthy Integration**:
- All 9 sensors created
- Sensors update every 15 minutes
- No errors in logs
- Sensor states match Harbor Lookout website
- Attributes populated with ship details
- TTS announcements work
- Automations trigger correctly

❌ **Unhealthy Integration**:
- Sensors show "unavailable"
- Logs show connection errors
- Sensors never update
- No attributes on sensors
- Integration shows "Failed to load"

## Getting Help

If tests fail:
1. Check Home Assistant logs for specific errors
2. Verify Harbor Lookout website is accessible
3. Try reloading the integration
4. Restart Home Assistant
5. Open an issue with:
   - Error logs
   - Sensor states
   - API test results
   - Home Assistant version

## API Field Reference (to be updated)

Once you test the API, update this section with actual field names:

**Note**: The integration currently expects these fields (adjust `api.py` if different):
- Ship identification: `name`, `mmsi`, `imo`
- Location: `latitude`, `longitude` (or `lat`, `lon`, `lng`)
- Movement: `speed`, `heading` (or `course`)
- Schedule: `eta`, `etd`, `arrivalTime`, `departureTime`
- Details: `type`, `cargo`, `destination`, `status`, `flag`/`nationality`
- Dimensions: `length`, `width`/`beam`

If the actual API uses different field names, update `api.py` → `parse_ship_data()` method accordingly.
