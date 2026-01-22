# Installation Instructions

## Quick Start

### Prerequisites
- Home Assistant 2023.1 or newer
- Internet connection to reach Harbor Lookout API
- (Optional) TTS service configured for announcements

### Installation Steps

1. **Download the integration**
   ```bash
   # Option A: Clone this repository
   git clone https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant.git
   cd Duluth-Ship-Tracker-for-HomAssistant

   # Option B: Download ZIP
   # Download from GitHub and extract
   ```

2. **Copy to Home Assistant**

   **If using Home Assistant OS / Supervised:**
   - Use File Editor add-on, Samba share, or SSH
   - Copy `custom_components/duluth_ship_tracker/` to `/config/custom_components/`

   **If using Home Assistant Container:**
   ```bash
   # From your docker host
   docker cp custom_components/duluth_ship_tracker/ homeassistant:/config/custom_components/
   ```

   **If using Home Assistant Core:**
   ```bash
   # From this repository directory
   cp -r custom_components/duluth_ship_tracker ~/.homeassistant/custom_components/
   ```

3. **Verify file structure**
   ```
   /config/custom_components/duluth_ship_tracker/
   ├── __init__.py
   ├── api.py
   ├── config_flow.py
   ├── const.py
   ├── coordinator.py
   ├── manifest.json
   ├── sensor.py
   └── strings.json
   ```

4. **Restart Home Assistant**
   - Go to **Settings** → **System** → **Restart** (top right menu)
   - Or: Developer Tools → YAML → Restart

5. **Add the integration**
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration** (bottom right)
   - Search for "**Duluth Ship Tracker**"
   - Click on it to add

6. **Configure options** (or use defaults)
   - Daily announcement time: `08:00` (8 AM)
   - Warning minutes before arrival/departure: `15`
   - TTS service: `tts.google_translate_say`
   - Click **Submit**

7. **Verify installation**
   - Integration should show as "Loaded"
   - 9 new sensors should be created
   - See [TESTING.md](TESTING.md) for detailed verification

## Adding Automations

### Option 1: Via Configuration Files

1. **Copy example automations**
   ```bash
   cat automations.yaml >> /config/automations.yaml
   ```

2. **Copy example scripts** (optional)
   ```bash
   cat scripts.yaml >> /config/scripts.yaml
   ```

3. **Reload automations**
   - **Developer Tools** → **YAML** → **Automations**

### Option 2: Via UI

1. Go to **Settings** → **Automations & Scenes**
2. Click **+ Create Automation**
3. Use examples from `automations.yaml` as reference
4. Paste YAML or build via UI

## Configuration Options

You can change these after installation:

1. **Settings** → **Devices & Services**
2. Find **Duluth Ship Tracker**
3. Click **Configure**
4. Adjust:
   - Daily announcement time
   - Warning time (minutes)
   - TTS service entity ID

## Updating the Integration

To update to a newer version:

1. **Backup your current installation** (optional but recommended)
   ```bash
   cp -r /config/custom_components/duluth_ship_tracker /config/custom_components/duluth_ship_tracker.backup
   ```

2. **Download new version**
   ```bash
   git pull  # if using git
   # or download new ZIP
   ```

3. **Copy new files** (overwrites old ones)
   ```bash
   cp -r custom_components/duluth_ship_tracker /config/custom_components/
   ```

4. **Restart Home Assistant**

5. **Check changelog** for any breaking changes

## Uninstalling

To completely remove the integration:

1. **Remove from Home Assistant**
   - **Settings** → **Devices & Services**
   - Find **Duluth Ship Tracker**
   - Click **⋮** → **Delete**

2. **Remove files** (optional, for clean uninstall)
   ```bash
   rm -rf /config/custom_components/duluth_ship_tracker
   ```

3. **Remove automations/scripts** (if added)
   - Edit `automations.yaml` and `scripts.yaml`
   - Remove Duluth Ship Tracker entries

4. **Restart Home Assistant**

## Troubleshooting Installation

### Integration doesn't appear in list
- Verify files are in correct location
- Check file permissions (should be readable)
- Check logs: **Settings** → **System** → **Logs**
- Try restarting Home Assistant again

### Setup fails with "cannot_connect"
- Verify internet connectivity
- Test API access: `curl https://prod-harbor-lookout-api-huckbngcchcfcwb8.centralus-01.azurewebsites.net/api/Display/shipsForDisplay`
- Check firewall rules
- See [TESTING.md](TESTING.md) for detailed troubleshooting

### Sensors not created
- Integration must show "Loaded" status first
- Check logs for errors during sensor setup
- Try reloading: **⋮** → **Reload** on the integration

### Permission denied errors
Fix file permissions:
```bash
chmod -R 755 /config/custom_components/duluth_ship_tracker
chown -R homeassistant:homeassistant /config/custom_components/duluth_ship_tracker
```

## Platform-Specific Notes

### Home Assistant OS / Supervised
- Use **File Editor** add-on or **Samba Share** for easy file access
- Advanced users can enable **SSH & Web Terminal** add-on

### Home Assistant Container (Docker)
- Files must be accessible inside container
- Use volume mounts: `-v /path/to/config:/config`
- Or use `docker cp` as shown above

### Home Assistant Core (Python venv)
- Direct file access available
- Usually installed at `~/.homeassistant/` or `/home/homeassistant/.homeassistant/`

## Next Steps

After installation:
1. Read [TESTING.md](TESTING.md) to verify everything works
2. Customize automations in `automations.yaml`
3. Add Lovelace cards (see README.md)
4. Configure notification services
5. Set up TTS on your preferred media players

## Support

If you encounter issues:
1. Check [TESTING.md](TESTING.md) for troubleshooting
2. Review [Home Assistant logs](http://homeassistant.local:8123/config/logs)
3. Open an issue on GitHub with:
   - Home Assistant version
   - Error logs
   - Installation method used
   - Steps to reproduce

## Links

- [README](README.md) - Full documentation
- [TESTING](TESTING.md) - Testing and troubleshooting
- [GitHub Issues](https://github.com/aarn5568/Duluth-Ship-Tracker-for-HomAssistant/issues)
- [Home Assistant Community](https://community.home-assistant.io/)
