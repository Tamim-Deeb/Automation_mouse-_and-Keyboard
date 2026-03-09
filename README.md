# Automation_mouse-_and-Keyboard
To automate clicks, drag, writing, reading from excel

## For End Users: Running the Portable Windows Application

### Download and Installation

1. **Download the application**
   - Go to the [Releases page](../../releases)
   - Download the latest `AutomationBuilder-windows.zip` file

2. **Extract the zip file**
   - Right-click the downloaded zip file
   - Select "Extract All..." (Windows)
   - Choose a location to extract the folder

3. **Run the application**
   - Open the extracted `AutomationBuilder` folder
   - Double-click `AutomationBuilder.exe`
   - The application will launch within a few seconds

**Important:** Keep all files in the `AutomationBuilder` folder together. Moving just the `.exe` file out of the folder will break the application.

### System Requirements

- **Operating System:** Windows 10 or later
- **Disk Space:** ~150 MB for the application folder
- **Permissions:** No administrator privileges required

### Troubleshooting

| Issue | Solution |
|-------|----------|
| SmartScreen blocks the exe | Click "More info" → "Run anyway" |
| Antivirus flags the exe | Add an exception for the AutomationBuilder folder |
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

See [specs/002-windows-exe-packaging/quickstart.md](specs/002-windows-exe-packaging/quickstart.md) for detailed build instructions.
