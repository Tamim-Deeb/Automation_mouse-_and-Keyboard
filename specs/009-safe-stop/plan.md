# Implementation Plan: Safe Stop (Esc Key Kill Switch)

**Branch**: `009-safe-stop` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/009-safe-stop/spec.md`

## Summary

Wire the existing `KillSwitch` class into the `WorkflowExecutor` loop so that pressing Esc during execution immediately stops the workflow. The kill switch already listens globally for Esc via pynput, but its `is_triggered()` state is never checked by the executor. This plan connects that signal to the executor's control flow, makes wait steps interruptible, and adds a polling mechanism in the execution panel to detect kill-switch triggers.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel)
**Storage**: N/A (no new storage)
**Testing**: pytest
**Target Platform**: macOS, Windows 10+
**Project Type**: Desktop app (tkinter GUI)
**Performance Goals**: Kill switch must halt execution within 1 second of Esc press
**Constraints**: Must not interfere with Esc key when no workflow is running; pynput keyboard listener only (mouse listener crashes on macOS)
**Scale/Scope**: Single-user desktop app

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | This feature IS the kill-switch implementation — directly fulfills the constitution's core safety requirement |
| II. Simplicity & Usability | PASS | No new configuration needed; Esc key is already the default kill-switch hotkey per constitution |
| III. Modular Extensibility | PASS | Changes are scoped to executor and execution panel; no existing modules are modified beyond their interfaces |
| IV. Data Integrity | PASS | Stop does not write data; Excel source is read-only |
| V. Minimal Critical-Path Testing | PASS | Kill-switch integration test already exists at `tests/integration/test_kill_switch.py`; will extend it |
| Kill-switch hotkey registered before automation | PASS | Already done in `execution_panel.py:135-136` |
| Timing guards (50ms minimum) | N/A | No new timing operations |
| Dry-run mode | N/A | Kill switch works in both dry-run and live mode |
| Logging | PASS | Executor already logs step start/complete/error; stop event will be logged |

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/009-safe-stop/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── engine/
│   ├── executor.py          # MODIFY: inject kill_switch, check between steps
│   ├── kill_switch.py       # EXISTING: no changes needed
│   └── step_registry.py     # EXISTING: no changes needed
├── automation/
│   └── wait.py              # MODIFY: add interruptible sleep method
├── gui/
│   ├── execution_panel.py   # MODIFY: poll kill_switch, trigger executor.stop()
│   └── ...
└── ...

tests/
├── integration/
│   ├── test_kill_switch.py  # EXTEND: add executor integration tests
│   └── test_executor.py     # EXTEND: add kill-switch stop tests
└── ...
```

**Structure Decision**: Single project layout (existing). No new files needed — all changes modify existing modules.
