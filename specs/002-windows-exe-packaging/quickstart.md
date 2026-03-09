# Quickstart: Windows Portable Application

**Feature Branch**: `002-windows-exe-packaging`

## For Developers: Building the Portable Folder

### Prerequisites
- Python 3.12 installed
- All project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller installed (`pip install pyinstaller`)

### Build Locally (Windows)

```bash
# From the repository root
python -m PyInstaller build/AutomationBuilder.spec
```

The output folder will be at `dist/AutomationBuilder/`. The main exe is `dist/AutomationBuilder/AutomationBuilder.exe`.

### Create a Distributable Zip

```bash
# Zip the folder for distribution
cd dist && powershell Compress-Archive -Path AutomationBuilder -DestinationPath AutomationBuilder-windows.zip
```

### Build via CI

Push to the `main` branch or create a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Download the `.zip` from the GitHub Actions artifacts tab or the Releases page.

## For End Users: Running the App

1. Download `AutomationBuilder-windows.zip` from the GitHub Releases page
2. Right-click the zip → "Extract All..." → choose a location
3. Open the extracted `AutomationBuilder` folder
4. Double-click `AutomationBuilder.exe`
5. Windows SmartScreen may show a warning — click "More info" → "Run anyway"
6. The app launches instantly (no extraction delay)

**Important**: Keep all files in the folder together. Moving just the `.exe` out of the folder will break the app.

## Verifying the Build

After building, verify on a clean Windows 10+ machine:

1. Copy the `AutomationBuilder` folder to a machine with no Python installed
2. Double-click `AutomationBuilder.exe` — the GUI should appear within 5 seconds
3. Import an Excel file — verify column headers display
4. Build a workflow with click, type, and wait steps
5. Run in dry-run mode — verify log output
6. Press Esc — verify kill-switch stops execution

## Troubleshooting

| Issue | Solution |
|-------|----------|
| SmartScreen blocks the exe | Click "More info" → "Run anyway" |
| Antivirus flags the exe | Add an exception for the AutomationBuilder folder |
| App doesn't start | Check Windows version is 10 or later |
| "Failed to execute script" error | Run from command line to see error output |
| Exe doesn't work after moving it | Keep all files in the folder together — don't move just the exe |
