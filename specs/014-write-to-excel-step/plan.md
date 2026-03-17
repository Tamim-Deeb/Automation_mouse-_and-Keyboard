# Implementation Plan: Write To Excel Step

**Branch**: `014-write-to-excel-step` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/014-write-to-excel-step/spec.md`

## Summary

Add a "Write To Excel" workflow step that writes data back to the same Excel file and sheet being processed. Two write modes: "Mark Done" (writes "x") and "Paste Clipboard" (writes clipboard content). The user selects a target column from the loaded headers. An `ExcelWriter` module handles opening the file in write mode, updating the cell, and saving.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: openpyxl (Excel read/write), pyperclip (clipboard), tkinter (GUI), pyautogui
**Storage**: Excel .xlsx files (openpyxl)
**Testing**: pytest
**Target Platform**: Windows desktop (PyInstaller), macOS/Linux dev
**Project Type**: Desktop application
**Performance Goals**: Write + save should complete in under 2 seconds per row
**Constraints**: Excel file must not be open in another application; openpyxl cannot write to read_only workbooks
**Scale/Scope**: Single user, single Excel file at a time, up to 10,000 rows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch remains active during write operations; write step is interruptible between steps |
| II. Simplicity & Usability | PASS | Two-option mode selector (Mark Done / Paste Clipboard) + column dropdown — minimal UI complexity |
| III. Modular Extensibility | PASS | ExcelWriter is a new independent module in `src/excel/writer.py`; does not modify ExcelReader |
| IV. Data Integrity | PASS | Writes target specific cells only; validates column exists at config time; saves after each write |
| V. Minimal Critical-Path Testing | PASS | Integration test for write pipeline planned |

## Project Structure

### Documentation (this feature)

```text
specs/014-write-to-excel-step/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── excel/
│   ├── reader.py          # Existing — read-only Excel access (unchanged)
│   └── writer.py          # NEW — write-mode Excel access
├── automation/
│   └── clipboard.py       # Existing — add paste() method
├── workflow/
│   └── models.py          # Existing — add WRITE_TO_EXCEL to StepType
├── engine/
│   ├── executor.py        # Existing — add row_number to handler context
│   └── step_registry.py   # Existing — register write_to_excel handler
├── gui/
│   ├── step_editors.py    # Existing — add write_to_excel editor form
│   └── workflow_panel.py  # Existing — add display format + step type button
└── main.py                # Existing — register write_to_excel handler

tests/
└── test_excel_writer.py   # NEW — integration test for ExcelWriter
```

**Structure Decision**: Follows existing single-project structure. New `ExcelWriter` module mirrors `ExcelReader` in `src/excel/`. Clipboard module gets a `paste()` method. All other changes integrate into existing files following established patterns.

## Complexity Tracking

No constitution violations. No complexity justification needed.
