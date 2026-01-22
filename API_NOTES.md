# API Field Mapping Notes

## Important: API Field Adjustment Required

The integration is built with **estimated field names** based on typical ship tracking APIs. You'll need to adjust the field mappings after testing with real API data.

## How to Test and Adjust

### Step 1: Test the API

Run the included test script to see actual API response:

```bash
python3 test_api.py
```

Or test in browser:
```
https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay
```

### Step 2: Review the Response

The test script will show:
- All available field names
- Example values for each field
- Data structure (list/dict)
- Sample ship data

### Step 3: Update Field Mappings

If the actual API uses different field names, edit:

**File: `custom_components/duluth_ship_tracker/api.py`**

Find the `parse_ship_data()` method (around line 55) and update field mappings:

```python
def parse_ship_data(self, ship: dict[str, Any]) -> dict[str, Any]:
    """Parse raw ship data into structured format."""
    return {
        "ship_name": ship.get("name"),  # ← Update if API uses different field
        "mmsi": ship.get("mmsi"),
        "imo": ship.get("imo"),
        # ... etc
    }
```

## Expected Fields (Update as Needed)

### Currently Mapped Fields

The integration expects these fields from the API:

| Integration Key | Expected API Field(s) | Alternative Names Tried |
|----------------|----------------------|------------------------|
| `ship_name` | `name` | `shipName`, `vesselName` |
| `ship_type` | `type` | `vesselType`, `shipType` |
| `cargo` | `cargo` | `cargoType`, `commoditySummary` |
| `destination` | `destination` | `destinationPort` |
| `arrival_time` | `arrivalTime` | `eta`, `estimatedArrival` |
| `departure_time` | `departureTime` | `etd`, `estimatedDeparture` |
| `latitude` | `latitude` | `lat` |
| `longitude` | `longitude` | `lon`, `lng` |
| `speed` | `speed` | `speedOverGround`, `sog` |
| `heading` | `heading` | `course`, `cog` |
| `status` | `status` | `navigationStatus`, `shipStatus` |
| `nationality` | `nationality` | `flag`, `country` |
| `length` | `length` | `shipLength` |
| `width` | `width` | `beam`, `shipWidth` |

## Common API Response Formats

### Format 1: List of Ships (Most Likely)
```json
[
  {
    "name": "Paul R. Tregurtha",
    "type": "Bulk Carrier",
    "eta": "2026-01-21T16:45:00Z",
    "status": "Underway",
    ...
  },
  {
    "name": "James R. Barker",
    ...
  }
]
```

### Format 2: Wrapped Response
```json
{
  "ships": [...],
  "lastUpdate": "...",
  "count": 12
}
```

If you see Format 2, update `api.py` → `get_ships()` to extract the ships array:
```python
data = await response.json()
ships = data.get("ships", [])  # Extract ships array
```

## Timestamp Formats

The integration handles multiple timestamp formats:

- ISO 8601: `2026-01-21T16:45:00Z`
- ISO without Z: `2026-01-21T16:45:00`
- Unix timestamp: `1737480300`
- Custom format: Add to `_parse_timestamp()` method

If timestamps aren't parsing correctly, check `api.py` → `_parse_timestamp()` and add the format used by the API.

## Status Values

The integration filters ships by status. Common status values:

**Moored/Docked** (ships in harbor):
- `"moored"`, `"anchored"`, `"at berth"`, `"docked"`

Update these in `api.py` → `get_ships_in_harbor()` if API uses different values.

## Real-World Example

After testing, you might find the API uses:
```json
{
  "vesselName": "Paul R. Tregurtha",  ← Not "name"
  "vesselType": "Bulk Carrier",       ← Not "type"
  "commodity": "Iron Ore",            ← Not "cargo"
  "expectedArrival": "2026-01-21...", ← Not "arrivalTime"
}
```

Then update `parse_ship_data()`:
```python
return {
    "ship_name": ship.get("vesselName"),     # ← Changed
    "ship_type": ship.get("vesselType"),     # ← Changed
    "cargo": ship.get("commodity"),          # ← Changed
    "arrival_time": self._parse_timestamp(ship.get("expectedArrival")),  # ← Changed
    # ...
}
```

## Testing After Changes

1. Edit `api.py` with correct field names
2. Copy updated file to Home Assistant
3. Reload integration: **Settings** → **Devices & Services** → Duluth Ship Tracker → **⋮** → **Reload**
4. Check sensor attributes to verify data is populating correctly

## Need Help?

If you need help mapping fields:

1. Run `python3 test_api.py` and save the output
2. Open a GitHub issue with the output
3. I can help create the correct field mappings

## Future Enhancement

Once we know the actual API structure, this integration can be enhanced to:
- Add more ship details (draft, beam, built year, etc.)
- Better status detection
- Historical tracking
- Route visualization
- And more!

---

**Note**: The integration will still work even if field names don't match - sensors will show "Unknown" or empty values until field mappings are corrected. The integration won't crash or fail, it just won't have complete data.
