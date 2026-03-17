# Research: Copy Field Step

## R1: Clipboard Clearing Approach

**Decision**: Use `pyperclip.copy('')` to clear the clipboard before selecting and copying

**Rationale**: pyperclip is a lightweight cross-platform clipboard library. Calling `copy('')` reliably clears the clipboard on Windows, macOS, and Linux. The project already uses pyautogui which has no clipboard API, so pyperclip fills this gap cleanly.

**Alternatives considered**:
- **Win32 API (ctypes)**: Rejected — Windows-only, not cross-platform
- **tkinter clipboard**: Rejected — requires a Tk root window reference, adds coupling to GUI layer
- **subprocess (xclip/pbcopy)**: Rejected — fragile, platform-specific shell commands

## R2: Sub-Action Delay Timing

**Decision**: 50ms delay between each sub-action (clear → select all → copy)

**Rationale**: 50ms matches the project's existing MIN_DELAY_MS constant in WaitModule and the constitution's timing guard minimum. This gives the OS enough time to process each clipboard/keyboard operation without feeling sluggish.

**Alternatives considered**:
- **No delay**: Rejected — clipboard operations may not complete before the next keystroke on slower systems
- **100ms**: Considered acceptable but 50ms is sufficient based on pyautogui's own internal timing

## R3: Step Handler Implementation Pattern

**Decision**: Implement as a standalone handler function registered in the global StepRegistry, following the existing pattern in main.py

**Rationale**: All existing step handlers follow this pattern — a function with signature `(step, session, row_data) -> None` registered via `register_step_handler()`. The Copy Field handler will call three operations in sequence: clipboard clear, pyautogui.hotkey('ctrl', 'a'), pyautogui.hotkey('ctrl', 'c').

**Alternatives considered**:
- **Composite step expanding to 3 sub-steps**: Rejected — adds complexity to the executor; a single handler is simpler and matches how other steps work
- **New module in src/automation/**: Decided to add clipboard.py for the clear operation, keeping automation capabilities modular per Constitution III
