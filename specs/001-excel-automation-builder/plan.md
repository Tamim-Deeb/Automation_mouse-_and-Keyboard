# Implementation Plan: Excel-Driven Desktop Automation Workflow Builder

**Branch**: `001-excel-automation-builder` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-excel-automation-builder/spec.md`

## Summary

Build a Python desktop application (tkinter GUI) that lets non-technical users
visually assemble automation workflows (click, double-click, type text, wait,
insert Excel column value, press hotkey), execute them row-by-row against an
imported Excel worksheet, and save/load workflows for reuse. The execution
engine uses pyautogui for mouse/keyboard simulation, openpyxl for Excel
reading, and pynput for kill-switch monitoring. A modular architecture
separates GUI, workflow engine, Excel reader, and input automation into
independent modules.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: tkinter (GUI, stdlib), pyautogui (mouse/keyboard
automation), openpyxl (Excel .xlsx reading), pynput (global hotkey
monitoring for kill-switch)
**Storage**: JSON files for workflow persistence, .xlsx files for data input
**Testing**: pytest (integration tests for critical paths per constitution)
**Target Platform**: macOS (primary dev), Windows compatible (pyautogui
cross-platform)
**Project Type**: Desktop application (single-window GUI)
**Performance Goals**: Handle worksheets up to 10,000 rows; inter-step
delay minimum 50ms configurable; kill-switch response < 2 seconds
**Constraints**: Offline-only, local file storage, no external services,
single-user
**Scale/Scope**: Single user, single workflow at a time, up to 10,000 rows
per execution

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Requirement | Status |
|---|-----------|------------|--------|
| I | Safety First | Kill-switch hotkey (Esc) registered before execution; halt after current step | PASS — FR-016 |
| I | Safety First | Fail-safe: no automation without active abort | PASS — FR-015, FR-016 |
| II | Simplicity & Usability | Configurable without modifying source code | PASS — GUI-driven workflow builder + JSON save/load |
| II | Simplicity & Usability | Low barrier for spreadsheet-skilled users | PASS — SC-006 targets 90% first-time success |
| III | Modular Extensibility | Independent composable modules | PASS — architecture separates gui/engine/excel/automation modules |
| III | Modular Extensibility | Adding new step type must not modify existing modules | PASS — step type registry pattern |
| IV | Data Integrity | Never corrupt source Excel data | PASS — read-only Excel access, no writes to source |
| IV | Data Integrity | Validate data before acting | PASS — edge cases define validation behavior |
| V | Minimal Critical-Path Testing | Integration test per module, pytest | PASS — will implement per module |
| — | Dry-run mode (Safety & Operational Constraints) | Every workflow MUST support dry-run flag | **ACTION NEEDED** — not in spec; adding FR-019 |
| — | Timing guards | Configurable delays minimum 50ms | PASS — assumptions section |
| — | Logging | Timestamped log file per run | PASS — FR-018 |

**Constitution gap resolved**: Adding FR-019 (dry-run mode) to the spec
during plan finalization. Dry-run mode logs intended actions to the
execution log without sending any mouse/keyboard events.

## Project Structure

### Documentation (this feature)

```text
specs/001-excel-automation-builder/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── workflow-file-schema.json
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py                  # Application entry point
├── gui/
│   ├── __init__.py
│   ├── app.py               # Main window, layout, menu
│   ├── workflow_panel.py    # Step list, add/reorder/delete
│   ├── step_editors.py      # Per-step-type parameter forms
│   ├── excel_panel.py       # Workbook import, sheet selection
│   ├── execution_panel.py   # Start/Stop, progress, start row
│   └── coordinate_picker.py # Click-to-capture overlay
├── engine/
│   ├── __init__.py
│   ├── executor.py          # Row-by-row execution loop
│   ├── step_registry.py     # Step type registration
│   └── kill_switch.py       # Global hotkey listener (pynput)
├── automation/
│   ├── __init__.py
│   ├── mouse.py             # Click, double-click via pyautogui
│   ├── keyboard.py          # Type text, hotkeys via pyautogui
│   └── wait.py              # Timed delays
├── excel/
│   ├── __init__.py
│   └── reader.py            # Workbook/sheet loading, formatted cell values
├── workflow/
│   ├── __init__.py
│   ├── models.py            # Workflow, WorkflowStep dataclasses
│   └── serializer.py        # JSON save/load
└── logging/
    ├── __init__.py
    └── action_logger.py     # Timestamped execution log

tests/
├── integration/
│   ├── test_excel_reader.py
│   ├── test_workflow_serializer.py
│   ├── test_executor.py
│   └── test_coordinate_picker.py
└── conftest.py
```

**Structure Decision**: Single-project layout. The desktop app is a
monolithic application with clear internal module boundaries (gui, engine,
automation, excel, workflow, logging). No need for multi-project structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| Out-of-bounds coords: skip instead of halt (Constitution IV) | Screen layout may change mid-execution; halting a multi-thousand-row run for a recoverable config issue is disproportionate | Halting would force users to restart from scratch, violating Simplicity principle (II). Skip + log warning preserves auditability. |

Dry-run gap addressed by adding FR-019.
