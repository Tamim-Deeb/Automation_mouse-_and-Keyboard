# Data Model: Excel-Driven Desktop Automation Workflow Builder

**Branch**: `001-excel-automation-builder`
**Date**: 2026-03-09

## Entities

### Workflow

Represents a saved, reusable automation sequence.

| Field       | Type         | Constraints                          |
|-------------|--------------|--------------------------------------|
| name        | string       | Required, user-provided              |
| steps       | list[Step]   | Ordered, 0..N steps allowed          |
| created_at  | datetime     | Set on first save                    |
| updated_at  | datetime     | Set on every save                    |

**Identity**: A workflow is uniquely identified by its file path on disk.
No internal ID is needed since workflows are single-file, single-user.

**Lifecycle**: Created (in-memory) → Saved (on disk) → Loaded → Modified
→ Re-saved. A workflow can exist in-memory without being saved.

### WorkflowStep

A single action in a workflow. Polymorphic by step type.

| Field      | Type   | Constraints                                  |
|------------|--------|----------------------------------------------|
| type       | enum   | One of: click, double_click, type_text, wait, insert_column_value, press_hotkey |
| order      | int    | Position in workflow (0-indexed)              |
| params     | dict   | Type-specific parameters (see below)          |

**Type-specific parameters**:

| Step Type           | Param Key    | Type   | Constraints                     |
|---------------------|-------------|--------|---------------------------------|
| click               | x           | int    | >= 0                            |
| click               | y           | int    | >= 0                            |
| double_click        | x           | int    | >= 0                            |
| double_click        | y           | int    | >= 0                            |
| type_text           | text        | string | Non-empty                       |
| wait                | duration_ms | int    | >= 50 (minimum timing guard)    |
| insert_column_value | column_name | string | Must match a worksheet header   |
| press_hotkey        | hotkey      | string | One of: Enter, Backspace, Esc, Tab, Shift+Tab, Ctrl+A, Ctrl+C, Ctrl+V |

**Validation rules**:
- `click` and `double_click`: x and y must be non-negative integers.
- `wait`: duration_ms must be >= 50 (constitution timing guard).
- `insert_column_value`: column_name validated against loaded worksheet
  headers at execution time (not at step creation time, since the Excel
  file may change).
- `press_hotkey`: value must be in the predefined hotkey list.

### ExcelDataSource

Represents the imported Excel workbook and selected worksheet.

| Field          | Type        | Constraints                       |
|----------------|-------------|-----------------------------------|
| file_path      | string      | Must be a valid .xlsx file path   |
| sheet_name     | string      | Must exist in the workbook        |
| headers        | list[str]   | Extracted from first row          |
| row_count      | int         | Data rows only (excluding header) |

**Constraints**:
- Maximum 10,000 data rows.
- Headers extracted from row 1; duplicate headers use first occurrence.
- File opened read-only; never modified.

### ExecutionSession

Represents a single run of a workflow against a data source.

| Field        | Type     | Constraints                              |
|--------------|----------|------------------------------------------|
| workflow     | Workflow | Required                                  |
| data_source  | ExcelDataSource | Required                           |
| start_row    | int      | >= 1, default 1 (first data row)         |
| current_row  | int      | Tracks progress during execution          |
| status       | enum     | One of: idle, running, stopped, completed |
| dry_run      | bool     | Default false; skips automation if true   |
| log_entries  | list     | Timestamped action records                |

**State transitions**:

```text
idle → running       (user clicks Start)
running → stopped    (user clicks Stop or presses kill-switch)
running → completed  (all rows processed)
stopped → idle       (ready for new execution)
completed → idle     (ready for new execution)
```

**Invariants**:
- Cannot transition from `idle` to `stopped` or `completed`.
- `current_row` only advances during `running` state.
- `log_entries` persist after execution ends (viewable by user).

### LogEntry

A single logged action within an execution session.

| Field     | Type     | Constraints                              |
|-----------|----------|------------------------------------------|
| timestamp | datetime | UTC, set at action time                  |
| row       | int      | Which data row was being processed       |
| step_type | string   | The step type that was executed           |
| detail    | string   | Human-readable description of the action |
| dry_run   | bool     | Whether this was a dry-run log entry     |

## Relationships

```text
Workflow 1───* WorkflowStep     (ordered list)
ExecutionSession 1───1 Workflow
ExecutionSession 1───1 ExcelDataSource
ExecutionSession 1───* LogEntry
```

## Data Volume Assumptions

- A typical workflow contains 3–20 steps.
- A typical Excel file contains 10–10,000 rows.
- A single execution session produces one log entry per step per row
  (e.g., 20 steps × 10,000 rows = 200,000 log entries max).
- Log entries are written to a file incrementally (not held in memory).
