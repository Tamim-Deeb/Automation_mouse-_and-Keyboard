# Automation_mouse-_and-Keyboard
To automate clicks, drag, writing, reading from excel

## For End Users: Running the Portable Windows Application

### Download

Download the latest version from the [Releases page](../../releases/latest) — click **AutomationMouseKeyboard-Windows.zip**.

### Running the App

1. Extract the downloaded zip file (right-click → "Extract All...")
2. Open the `AutomationMouseKeyboard` folder
3. Double-click `AutomationMouseKeyboard.exe` to launch the app
4. That's it — no installation needed

**Important:** Do not move `AutomationMouseKeyboard.exe` out of its folder. It needs the other files next to it to work.

### System Requirements

- **Operating System:** Windows 10 or later
- **Disk Space:** ~150 MB for the application folder
- **Permissions:** No administrator privileges required

### Troubleshooting

| Issue | Solution |
|-------|----------|
| SmartScreen blocks the exe | Click "More info" → "Run anyway" |
| Antivirus flags the exe | Add an exception for the AutomationMouseKeyboard folder |
| App doesn't start | Ensure Windows version is 10 or later |
| "Failed to execute script" error | Run from command prompt to see error details |
| Exe doesn't work after moving | Keep all files in the folder together |

### Quick Start Guide

1. **Import an Excel file**
   - Click "Import Excel" button
   - Select your `.xlsx` file
   - Choose a sheet from the dropdown

2. **Build a workflow**
   - Add steps: Click, Type Text, Wait, Insert Column Value, Press Hotkey
   - Configure each step with your parameters
   - Use column names from your Excel file for dynamic values

3. **Run the workflow**
   - Click "Run" to execute the workflow
   - Use "Dry Run" mode to test without actual actions
   - Press `Esc` key at any time to stop execution

4. **Save and load workflows**
   - Use "File → Save Workflow" to save your work
   - Use "File → Open Workflow" to load a saved workflow

## For Developers

### Building the Portable Application

This project uses PyInstaller to create a self-contained Windows executable that doesn't require Python installation.

#### Prerequisites

- Python 3.10+ installed (for building only — end users don't need Python)
- Windows machine (or Windows VM) for building the Windows executable

#### Installation

1. Install runtime dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install build dependencies:
   ```bash
   pip install -r requirements-build.txt
   ```

#### Building the Application

1. Create the application icon (if not already created):
   ```bash
   python create_icon.py
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

3. Find the output in `dist/AutomationMouseKeyboard/`:
   - `AutomationMouseKeyboard.exe` — the main executable
   - `_internal/` — bundled dependencies (must stay in the same folder)

#### Distributing to Users

1. Zip the entire `dist/AutomationMouseKeyboard/` folder
2. Share the zip file with users (email, download link, USB drive)
3. Users extract the zip and double-click `AutomationMouseKeyboard.exe`

#### Build Script Details

The `build.py` script:
- Checks prerequisites (spec file, icon, dependencies)
- Cleans previous build artifacts
- Runs PyInstaller with the `.spec` file
- Validates the build output
- Prints success/failure summary

The `AutomationMouseKeyboard.spec` file configures:
- Entry point: `src/main.py`
- One-folder mode (portable directory distribution)
- Windowed mode (no console window)
- Custom icon from `assets/app.ico`
- Hidden imports for pyautogui, pynput, openpyxl submodules

#### Testing the Build

1. Copy the `dist/AutomationMouseKeyboard/` folder to a machine without Python installed
2. Double-click `AutomationMouseKeyboard.exe`
3. Verify:
   - App window appears (no console window)
   - App icon shows in taskbar
   - Can load an Excel file
   - Can create and save a workflow
   - Can execute a workflow (mouse/keyboard automation works)
   - Kill switch (Esc key) works during execution

#### Troubleshooting Build Issues

- **"Windows protected your PC" warning**: Click "More info" → "Run anyway" (app is not code-signed)
- **Missing module errors**: Check `AutomationMouseKeyboard.spec` for hidden imports and add the missing module
- **App crashes silently**: Check for a startup error dialog; if none appears, run from command line to see stderr output

For more details, see [specs/003-portable-app/quickstart.md](specs/003-portable-app/quickstart.md).
