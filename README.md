# Shadowplay Activator

## Note
Updated October 2025 to work after recent small Instant Replay update.

## Installation

1. **Download the `shadowplay_activator.exe` file**
   - Click the green `<> Code` button above
   - Select `Download ZIP`
   - Extract the files (you can delete everything except the `.exe` file)

2. **Place the executable file** wherever you want on your computer for safekeeping

3. **Run it once** (this will automatically add it to your startup programs)

## Configuration

**Important:** Make sure your hotkey/shortcut to "Toggle Instant Replay On/Off" is set to `Alt+Shift+F10`

To set this hotkey:
- Open the Nvidia overlay menu
- Navigate to: **Settings → Shortcuts → Record** (about halfway down the screen)
- Set the hotkey to `Alt+Shift+F10`

## Done!

From now on, about 30 seconds after you start your computer and log in, the program will:
- Check if Shadowplay is already running
- If not, automatically activate it by simulating the hotkey

## Further Info

This script is designed **only** to ensure that 'Instant Replay' (aka 'Shadowplay') is turned on just after your computer launches. 

**Limitations:**
- It will **not** turn Instant Replay back on if disabled by other programs (e.g., Netflix or other streaming platforms)
- Only works on Windows PCs with Nvidia App installed and the overlay running
- Requires the hotkey set to `Alt+Shift+F10`

**Important:** Each time you move the program to a new location, run it manually once so it can update its location in Windows startup programs.

## Debugging

This script works by searching for a temp file in a specific location. If the program thinks Shadowplay isn't running when it actually is (i.e. it turns off your shadowplay!), your temporary files may be in a different location than the default.

### Fix:

1. Open the Nvidia overlay menu
2. **Turn off** Instant Replay/Shadowplay
3. Navigate to: **Settings (⚙️) → Files and Disk Space** 
4. Click **Select Temporary files location**
5. Navigate to: `C:\Users\your_username\AppData\Local\Temp`
6. Save the settings

This will ensure the temp files are created in the expected location.