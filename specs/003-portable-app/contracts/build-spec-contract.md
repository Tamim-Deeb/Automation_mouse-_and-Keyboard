# Build Specification Contract

**Purpose**: Defines the interface between the build script and PyInstaller configuration.

## PyInstaller Spec File Contract

The `.spec` file must configure:

| Parameter       | Value                          | Required |
|-----------------|--------------------------------|----------|
| `name`          | `AutomationMouseKeyboard`      | Yes      |
| `entrypoint`    | `src/main.py`                  | Yes      |
| `console`       | `False` (windowed mode)        | Yes      |
| `onefile`       | `False` (one-folder mode)      | Yes      |
| `icon`          | Path to `.ico` file            | Yes      |
| `hidden_imports`| Platform-specific module list   | Yes      |

## Build Script Contract

**Input**: No arguments required (configuration in spec file)
**Output**: A folder in `dist/` containing the portable app
**Exit codes**:
- `0`: Build successful
- Non-zero: Build failed (error message on stderr)

## Startup Error Handler Contract

When running as a frozen (packaged) executable:
- Uncaught exceptions at startup must be caught
- Error must be displayed in a tkinter messagebox (not printed to missing console)
- Dialog title: "Startup Error"
- Dialog body: User-friendly message + brief error detail
