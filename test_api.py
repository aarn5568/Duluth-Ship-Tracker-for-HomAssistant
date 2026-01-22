#!/usr/bin/env python3
"""Test script to fetch and display Harbor Lookout API data."""
import json
import sys
import urllib.request
from datetime import datetime

API_URL = "https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay"

def test_api():
    """Test the Harbor Lookout API."""
    print("=" * 80)
    print("Testing Harbor Lookout API Connection")
    print("=" * 80)
    print(f"\nAPI URL: {API_URL}\n")

    try:
        # Make request
        print("Fetching data...")
        req = urllib.request.Request(
            API_URL,
            headers={
                'User-Agent': 'Mozilla/5.0 (Home Assistant Duluth Ship Tracker)',
                'Accept': 'application/json'
            }
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

        print(f"✓ Successfully fetched data!")
        print(f"✓ Response status: {response.status}")
        print(f"✓ Content type: {response.headers.get('Content-Type')}")

        # Analyze data structure
        print("\n" + "=" * 80)
        print("DATA ANALYSIS")
        print("=" * 80)

        if isinstance(data, list):
            print(f"\n✓ Received list with {len(data)} items")

            if len(data) > 0:
                print("\n" + "-" * 80)
                print("FIRST SHIP EXAMPLE (raw data):")
                print("-" * 80)
                print(json.dumps(data[0], indent=2))

                print("\n" + "-" * 80)
                print("ALL FIELD NAMES FOUND:")
                print("-" * 80)
                all_keys = set()
                for ship in data:
                    if isinstance(ship, dict):
                        all_keys.update(ship.keys())

                for key in sorted(all_keys):
                    # Show example values from first ship that has this key
                    example = None
                    for ship in data:
                        if key in ship and ship[key] is not None:
                            example = ship[key]
                            break
                    example_str = f" (e.g., {example})" if example else ""
                    print(f"  - {key}{example_str}")

                print("\n" + "-" * 80)
                print("SHIP NAMES:")
                print("-" * 80)
                for i, ship in enumerate(data[:10], 1):  # First 10 ships
                    # Try to find the name field
                    name = ship.get('name') or ship.get('shipName') or ship.get('vesselName') or 'Unknown'
                    status = ship.get('status') or ship.get('shipStatus') or 'Unknown'
                    print(f"  {i}. {name} - Status: {status}")

                if len(data) > 10:
                    print(f"  ... and {len(data) - 10} more ships")

        elif isinstance(data, dict):
            print(f"\n✓ Received dictionary with {len(data)} keys")
            print("\nKeys found:")
            for key in data.keys():
                print(f"  - {key}")
            print("\nFull data:")
            print(json.dumps(data, indent=2))

        else:
            print(f"\n✗ Unexpected data type: {type(data)}")
            print(data)

        print("\n" + "=" * 80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 80)
        return True

    except urllib.error.HTTPError as e:
        print(f"\n✗ HTTP Error: {e.code} - {e.reason}")
        print(f"Response body: {e.read().decode()}")
        return False

    except urllib.error.URLError as e:
        print(f"\n✗ URL Error: {e.reason}")
        return False

    except json.JSONDecodeError as e:
        print(f"\n✗ JSON Decode Error: {e}")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
