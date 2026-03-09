# Quickstart: Portable App Distribution

**Feature**: 003-portable-app
**Date**: 2026-03-09

## Prerequisites

- Python 3.10+ installed (for building only — end users don't need Python)
- All project dependencies installed: `pip install -r requirements.txt`
- Windows machine (or cross-compilation setup) for building the Windows executable

## Building the Portable App

1. **Install build dependencies** (if not already):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**:
   ```bash
   python build.py
   ```

3. **Find the output** in `dist/AutomationMouseKeyboard/`:
   - `AutomationMouseKeyboard.exe` — the main executable
   - `_internal/` — bundled dependencies (must stay in the same folder)

## Distributing to Users

1. Zip the entire `dist/AutomationMouseKeyboard/` folder
2. Share the zip file with users (email, download link, USB drive)
3. Users extract the zip and double-click `AutomationMouseKeyboard.exe`

## Testing the Build

1. Copy the `dist/AutomationMouseKeyboard/` folder to a machine without Python installed
2. Double-click `AutomationMouseKeyboard.exe`
3. Verify:
   - App window appears (no console window)
   - App icon shows in taskbar
   - Can load an Excel file
   - Can create and save a workflow
   - Can execute a workflow (mouse/keyboard automation works)
   - Kill switch (Esc key) works during execution

## Troubleshooting

- **"Windows protected your PC" warning**: Click "More info" → "Run anyway" (app is not code-signed)
- **Missing module errors**: Check `build.py` for hidden imports and add the missing module
- **App crashes silently**: Check for a startup error dialog; if none appears, run from command line to see stderr output
