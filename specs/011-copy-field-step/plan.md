# Implementation Plan: Copy Field Step

**Branch**: `011-copy-field-step` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/011-copy-field-step/spec.md`

## Summary

Add a new "Copy Field" step type to the workflow builder. When executed, it performs three sub-actions in sequence: clear clipboard, Ctrl+A (select all), Ctrl+C (copy). This is a zero-parameter composite step that simplifies a common 3-step pattern into one click.

## Technical Context

**Language/Version**: Python 3.10+ (existing)
**Primary Dependencies**: pyautogui (keyboard automation), pyperclip (clipboard clearing), tkinter (GUI)
**Storage**: N/A (no new storage)
**Testing**: pytest
**Target Platform**: Windows 10+ (primary), macOS/Linux (secondary)
**Project Type**: Desktop application (tkinter GUI)
**Performance Goals**: Sub-action delay of 50-100ms between clipboard clear, Ctrl+A, Ctrl+C
**Constraints**: Must integrate with existing step registry, serialization, and step editor systems
**Scale/Scope**: Single-user desktop application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Step executes within existing kill-switch framework; checked between steps |
| II. Simplicity & Usability | PASS | Zero-parameter step — user adds it from dropdown with no configuration |
| III. Modular Extensibility | PASS | New step type registered via existing StepRegistry; no modification to existing modules |
| IV. Data Integrity | PASS | Reads from focused field only; does not write to external data sources |
| V. Minimal Critical-Path Testing | PASS | One integration test needed demonstrating clipboard capture |

**Gate result**: ALL PASS.

## Project Structure

### Documentation (this feature)

```text
specs/011-copy-field-step/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── automation/
│   └── clipboard.py         # NEW: Clipboard operations (clear)
├── workflow/
│   └── models.py            # Add COPY_FIELD to StepType enum
├── engine/
│   └── step_registry.py     # Register copy_field handler (in main.py registration)
└── gui/
    └── step_editors.py      # Add Copy Field to step type dropdown (no params UI)

src/main.py                   # Register copy_field step handler
```

**Structure Decision**: Single project layout. One new file (`src/automation/clipboard.py`) for clipboard operations. All other changes modify existing files.

## Complexity Tracking

No constitution violations — this section is not applicable.
