# Research: Excel-Driven Desktop Automation Workflow Builder

**Branch**: `001-excel-automation-builder`
**Date**: 2026-03-09

## R1: GUI Framework for Python Desktop App

**Decision**: tkinter (Python standard library)

**Rationale**: tkinter ships with Python — zero additional dependencies for
the GUI layer. It supports all required widgets: listbox for step ordering,
entry fields for parameters, buttons, progress bars, and file dialogs. The
constitution's Simplicity principle favors minimal dependencies. The app is
a single-window tool, not a complex multi-view application, so tkinter's
capabilities are sufficient.

**Alternatives considered**:
- **PyQt6 / PySide6**: More polished look, richer widget set, but adds a
  large dependency (~50MB) and GPL/LGPL licensing complexity. Overkill for
  this scope.
- **wxPython**: Cross-platform native look, but less widely used, harder to
  install on some platforms.
- **Dear PyGui**: GPU-accelerated, but unusual for form-based apps and adds
  complexity.

## R2: Excel Reading — Formatted Cell Values

**Decision**: openpyxl with `number_format` inspection for formatted output

**Rationale**: openpyxl is the constitution-mandated Excel library. To get
displayed/formatted text (per clarification Q5), we read the cell's value
and its `number_format` attribute, then apply Python formatting to produce
the string the user sees in Excel. For dates, openpyxl returns datetime
objects which we format using the cell's number format. For numbers, we
apply the format pattern.

**Alternatives considered**:
- **xlrd**: Only supports .xls (legacy), not .xlsx.
- **pandas**: Heavy dependency for simple row iteration. Adds numpy
  transitively. Violates simplicity principle.
- **openpyxl read_only mode**: For 10,000-row worksheets, read_only=True
  enables streaming reads with lower memory. We will use this mode for
  execution but regular mode for header inspection.

## R3: Mouse/Keyboard Automation Library

**Decision**: pyautogui (constitution-mandated)

**Rationale**: pyautogui provides cross-platform mouse click, move, type,
and hotkey functions. It includes a built-in FAILSAFE (moving mouse to
corner aborts) which complements our Esc kill-switch. Character-by-character
typing uses `pyautogui.write()` for ASCII and `pyautogui.typewrite()` for
special handling. For hotkeys, `pyautogui.hotkey()` handles combos like
Ctrl+V natively.

**Alternatives considered**:
- **pydirectinput**: Windows-only, uses DirectInput. Not cross-platform.
- **keyboard library**: Global hotkey support but requires root/admin on
  some platforms. We use pynput for the kill-switch listener instead.

## R4: Kill-Switch Implementation

**Decision**: pynput global keyboard listener in a daemon thread

**Rationale**: pynput's `keyboard.Listener` runs in a background thread and
detects key presses globally (even when the app window is not focused). This
is critical because during automation, the app window loses focus. The
listener sets a threading Event that the executor checks between steps.
Response time < 2 seconds is achievable since the check happens after each
step completes.

**Alternatives considered**:
- **pyautogui.FAILSAFE** (mouse-corner): Already enabled as secondary
  failsafe, but not user-friendly as primary mechanism.
- **keyboard library**: Requires elevated privileges on Linux/macOS.
  pynput handles this more gracefully.

## R5: Workflow Persistence Format

**Decision**: JSON files (.json extension)

**Rationale**: JSON is human-readable, easily debuggable, and requires no
additional dependencies (stdlib `json` module). The workflow data model is
a simple ordered list of typed step objects — a natural fit for JSON.
The constitution's Simplicity principle favors a format users can inspect
if needed.

**Alternatives considered**:
- **YAML**: More readable for complex configs, but requires PyYAML
  dependency.
- **SQLite**: Overkill for single-file workflow storage.
- **Pickle**: Not human-readable, security risk with untrusted files.

## R6: Click-to-Capture Coordinate Picker

**Decision**: Transparent fullscreen tkinter overlay with click handler

**Rationale**: When the user clicks "Pick" for a coordinate field, the app
creates a semi-transparent fullscreen window on top of all other windows.
The user clicks the desired screen location, the overlay captures the
(x, y) coordinates, closes itself, and populates the coordinate fields.
This approach works within tkinter without additional dependencies.

**Alternatives considered**:
- **Minimize app + global mouse hook**: User clicks anywhere while app is
  minimized. More complex state management, harder to cancel.
- **Screenshot + click on image**: Requires image display, adds complexity.
  Closer to OCR territory (out of scope).

## R7: Dry-Run Mode

**Decision**: Boolean flag on ExecutionSession; executor skips all
pyautogui/pynput calls and logs "DRY-RUN" prefix for each action

**Rationale**: Constitution requires every workflow to support dry-run.
Implementation is straightforward: the executor checks a `dry_run` flag
before each automation call. All logging still occurs with a [DRY-RUN]
prefix, allowing users to verify the workflow logic and data bindings
without affecting the desktop.

**Alternatives considered**:
- **Mock automation module**: Swap in a no-op module. More modular but
  adds complexity for a simple flag check. Could be a future refactor if
  more execution modes are needed.
