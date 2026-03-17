# Implementation Plan: Default Step Delay

**Branch**: `010-default-step-delay` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/010-default-step-delay/spec.md`

## Summary

Add a "Delay between steps" setting to the execution panel that inserts a configurable pause (default 200ms) after each workflow step during execution. The delay is an execution-time setting — not a workflow step — and persists across sessions via a simple JSON preferences file.

## Technical Context

**Language/Version**: Python 3.10+ (existing)
**Primary Dependencies**: pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel)
**Storage**: JSON preferences file (~/.automation-mouse/preferences.json) for delay persistence
**Testing**: pytest
**Target Platform**: Windows 10+ (primary), macOS/Linux (secondary)
**Project Type**: Desktop application (tkinter GUI)
**Performance Goals**: Delay accuracy within 50ms of configured value
**Constraints**: Delay must be interruptible by kill switch (Esc); minimum 0ms, default 200ms
**Scale/Scope**: Single-user desktop application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Delay uses interruptible sleep via kill switch — Esc stops execution during delay pauses |
| II. Simplicity & Usability | PASS | Single input field in execution panel; no code modification needed to use; 200ms sensible default |
| III. Modular Extensibility | PASS | Delay logic stays in executor; preferences are a standalone utility; no existing modules modified beyond their interfaces |
| IV. Data Integrity | PASS | Feature does not read/write external data sources; preferences file is append-only settings |
| V. Minimal Critical-Path Testing | PASS | Integration test needed for delay application during execution; unit test for preferences persistence |

**Safety & Operational Constraints**:
- Kill-switch hotkey: Esc key remains active during delay pauses (uses existing `interruptible_sleep`)
- Timing guards: Default delay of 200ms satisfies minimum 50ms timing guard requirement
- Dry-run mode: Delay applies in dry-run mode for realistic simulation

**Gate result**: ALL PASS — no violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/010-default-step-delay/
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
│   └── executor.py          # Add step_delay_ms parameter + delay after each step
├── gui/
│   └── execution_panel.py   # Add "Delay between steps" input field
├── automation/
│   └── wait.py              # Reuse existing interruptible_sleep()
└── preferences/
    └── preferences.py       # NEW: Simple JSON preferences load/save

tests/
└── (integration test for delay behavior)
```

**Structure Decision**: Single project layout. Only one new file (`src/preferences/preferences.py`) needed. All other changes modify existing files.

## Complexity Tracking

No constitution violations — this section is not applicable.
