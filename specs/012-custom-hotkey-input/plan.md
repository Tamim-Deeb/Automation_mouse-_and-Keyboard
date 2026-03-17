# Implementation Plan: Custom Hotkey Input

**Branch**: `012-custom-hotkey-input` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/012-custom-hotkey-input/spec.md`

## Summary

Add two freeform text input boxes ("Modifier (optional)" and "Key") to the Press Hotkey step editor, enabling users to type custom key combinations (e.g., Ctrl+F1, Ctrl+Shift+F1, F5) beyond the predefined dropdown. The modifier box supports multiple modifiers separated by "+". Custom input takes priority over the dropdown when the Key box is filled. The execution handler parses the custom hotkey string and calls pyautogui.hotkey() with the parsed keys.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pyautogui (keyboard automation), tkinter (GUI), pynput (kill-switch)
**Storage**: JSON workflow files (existing serializer)
**Testing**: pytest (manual integration testing for GUI)
**Target Platform**: Windows, macOS (desktop)
**Project Type**: Desktop application
**Performance Goals**: N/A (single keypresses, no throughput concerns)
**Constraints**: Must work with existing kill-switch suppress/unsuppress for Esc key steps
**Scale/Scope**: Single feature addition — 4 files modified, 0 new files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch remains active. Custom Esc hotkey already handled by suppress/unsuppress mechanism. |
| II. Simplicity & Usability | PASS | Two input boxes are intuitive. Dropdown preserved for common hotkeys. No code modification needed to use custom hotkeys. |
| III. Modular Extensibility | PASS | Changes are localized to step editor (GUI), keyboard automation (execution), and step handler registration. No existing modules modified in incompatible ways. |
| IV. Data Integrity | PASS | Custom hotkey strings validated at save time (Key required). Serialization uses existing JSON workflow format. |
| V. Minimal Critical-Path Testing | PASS | Manual quickstart test covers the critical path. No new test infrastructure needed. |

All gates pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/012-custom-hotkey-input/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── automation/
│   └── keyboard.py          # Add press_custom_hotkey() method
├── gui/
│   └── step_editors.py      # Add modifier + key input boxes to hotkey editor
├── workflow/
│   └── models.py            # No changes needed (hotkey stored as string in params)
├── engine/
│   └── step_registry.py     # No changes needed (handler registered in main.py)
└── main.py                  # Update press_hotkey_handler to support custom strings
```

**Structure Decision**: Existing single-project structure. No new files needed — all changes modify existing files.

## Complexity Tracking

No constitution violations. Table omitted.
