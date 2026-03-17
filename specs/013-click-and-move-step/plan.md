# Implementation Plan: Click And Move Step

**Branch**: `013-click-and-move-step` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/013-click-and-move-step/spec.md`

## Summary

Add a "Click And Move" (drag) step type that presses the left mouse button at start coordinates, moves to end coordinates, and releases. The step editor shows two coordinate groups (Start X/Y, End X/Y) each with its own "Pick" button using the same coordinate picker as the Click step. The mouse automation layer uses pyautogui's `moveTo` with `mouseDown`/`mouseUp` or the `drag`/`moveTo` API to perform the drag.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pyautogui (mouse automation), tkinter (GUI), pynput (kill-switch)
**Storage**: JSON workflow files (existing serializer)
**Testing**: pytest (manual integration testing for GUI)
**Target Platform**: Windows, macOS (desktop)
**Project Type**: Desktop application
**Performance Goals**: N/A (single drag operations, no throughput concerns)
**Constraints**: Must reuse existing coordinate picker callback pattern from Click step
**Scale/Scope**: Single feature addition — 4 files modified, 0 new files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch remains active during drag operations. Drag is interruptible via Esc kill-switch. |
| II. Simplicity & Usability | PASS | Two Pick buttons mirror the Click step UX — familiar pattern. No code modification needed to use drag steps. |
| III. Modular Extensibility | PASS | New `drag()` method added to existing MouseAutomation module. New step type registered via existing StepRegistry pattern. No existing modules broken. |
| IV. Data Integrity | PASS | Four integer coordinates validated at save time. Serialization uses existing JSON workflow format. |
| V. Minimal Critical-Path Testing | PASS | Manual quickstart test covers the critical drag path. |

All gates pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/013-click-and-move-step/
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
│   └── mouse.py             # Add drag() method
├── gui/
│   ├── step_editors.py      # Add drag coordinate fields (start + end with Pick buttons)
│   └── workflow_panel.py    # Add Click And Move display format
├── workflow/
│   └── models.py            # Add CLICK_AND_MOVE to StepType enum + validation
└── main.py                  # Register click_and_move_handler
```

**Structure Decision**: Existing single-project structure. No new files — all changes modify existing files.

## Complexity Tracking

No constitution violations. Table omitted.
