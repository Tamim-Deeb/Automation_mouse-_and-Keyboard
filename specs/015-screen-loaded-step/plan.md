# Implementation Plan: Screen Loaded Step

**Branch**: `015-screen-loaded-step` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/015-screen-loaded-step/spec.md`

## Summary

Add a "Screen Loaded" workflow step that verifies screen content is ready before continuing. The step clears the clipboard, drags to select text at user-specified coordinates, copies (Ctrl+C), and checks if the clipboard has content. If empty, it retries at 1-second intervals up to a configurable max tries. If max tries exceeded, the workflow stops. The step handler runs the retry loop inline, using existing clipboard, mouse drag, and hotkey modules.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pyautogui (mouse drag + Ctrl+C), pyperclip (clipboard), tkinter (GUI), pynput (kill-switch)
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Windows desktop (PyInstaller), macOS/Linux dev
**Project Type**: Desktop application
**Performance Goals**: Each attempt cycle (clear + drag + copy + check) completes in under 500ms excluding the 1-second retry wait
**Constraints**: Kill-switch must remain responsive during retry waits
**Scale/Scope**: Single user, up to 10 max tries typical

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch respected during retry waits via interruptible sleep; workflow stops on max tries exceeded |
| II. Simplicity & Usability | PASS | Reuses Click And Move coordinate picker pattern; single max tries field; no code changes needed by user |
| III. Modular Extensibility | PASS | Handler logic self-contained; uses existing clipboard, mouse, and keyboard modules without modification |
| IV. Data Integrity | PASS | Does not modify any data; only reads clipboard state |
| V. Minimal Critical-Path Testing | PASS | Handler logic is testable via existing step handler pattern |

## Project Structure

### Documentation (this feature)

```text
specs/015-screen-loaded-step/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── workflow/
│   └── models.py          # Existing — add SCREEN_LOADED to StepType + validation
├── engine/
│   ├── executor.py        # Existing — add logging format for SCREEN_LOADED
│   └── step_registry.py   # Existing — register screen_loaded handler
├── gui/
│   ├── step_editors.py    # Existing — add screen_loaded editor (coords + max tries)
│   └── workflow_panel.py  # Existing — add display format + step type button
└── main.py                # Existing — register screen_loaded handler with retry loop
```

**Structure Decision**: Follows existing single-project structure. No new modules needed — the handler orchestrates existing clipboard, mouse, and keyboard modules inline.

## Complexity Tracking

No constitution violations. No complexity justification needed.
