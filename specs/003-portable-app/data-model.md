# Data Model: Portable App Distribution

**Feature**: 003-portable-app
**Date**: 2026-03-09

## Entities

### App Package (Build Output)

The distributable folder produced by the build process.

| Attribute        | Description                                              |
|------------------|----------------------------------------------------------|
| Name             | Folder name matching the app name                        |
| Executable       | The main `.exe` file users double-click to launch        |
| Dependencies     | Bundled Python runtime, libraries, and platform binaries |
| Icon             | Application icon embedded in the executable              |
| Version          | App version identifier (for future compatibility checks) |

**Structure**:
```
AutomationMouseKeyboard/
├── AutomationMouseKeyboard.exe   # Main executable
├── _internal/                    # PyInstaller runtime dependencies
│   ├── python312.dll
│   ├── tkinter/
│   ├── pyautogui/
│   ├── openpyxl/
│   ├── pynput/
│   └── ...
└── (icon and metadata)
```

**Constraints**:
- The folder must be fully self-contained — no external dependencies required
- The executable must work from any filesystem location
- No files should require write access to the app folder at runtime

### Workflow File (Unchanged)

Existing entity from the current app. No changes needed for portability — workflow files are already JSON-based and use relative/user-chosen paths via file dialogs.

### Build Configuration (New)

The PyInstaller spec file that controls the build process.

| Attribute       | Description                                    |
|-----------------|------------------------------------------------|
| Entry point     | Path to `src/main.py`                          |
| Hidden imports  | List of modules PyInstaller can't auto-detect  |
| Icon path       | Path to the `.ico` file                        |
| Console mode    | Windowed (no console window)                   |
| Output mode     | One-folder (`onedir`)                          |

## State Transitions

### Build Process

```
Source Code → [Build Script] → PyInstaller Build → [Success] → App Package Folder
                                                 → [Failure] → Build Error (logged)
```

### App Startup (Packaged)

```
User Opens .exe → [Frozen Check] → Initialize Tkinter → Show Main Window → Ready
                                 → [Error] → Show Error Dialog → Exit
```

## Relationships

- **Build Configuration** → produces → **App Package**
- **App Package** → contains → **Executable** + **Dependencies**
- **Executable** → reads/writes → **Workflow Files** (via user file dialogs)
