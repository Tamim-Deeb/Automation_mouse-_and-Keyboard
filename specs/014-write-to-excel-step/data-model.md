# Data Model: Write To Excel Step

## Entities

### WriteToExcelStep (extends WorkflowStep)

A workflow step that writes a value to a specific column in the current Excel row.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| type | StepType | Always `WRITE_TO_EXCEL` | Must equal StepType.WRITE_TO_EXCEL |
| order | int | Position in workflow | Non-negative integer |
| params.column_name | string | Target column header name | Non-empty; must exist in loaded Excel headers |
| params.write_mode | string | Write mode identifier | Must be "mark_done" or "paste_clipboard" |

### ExcelWriter

Module for writing values to Excel cells. Stateless — opens, writes, saves, and closes on each call.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| write_cell | file_path: str, sheet_name: str, row: int, column_name: str, value: str | bool | Opens workbook, finds column by header name, writes value to cell at (row, column), saves, closes. Returns True on success. |

### ClipboardModule (extended)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| clear | — | None | Existing: clears clipboard |
| paste | — | str | NEW: returns current clipboard content as string |

## Relationships

- **WriteToExcelStep** → uses **ExcelWriter** to perform the write operation
- **WriteToExcelStep** (paste_clipboard mode) → uses **ClipboardModule.paste()** to get clipboard content
- **WriteToExcelStep** → references **ExcelDataSource** (via session) for file_path and sheet_name
- **WorkflowExecutor** → passes session (with current_row) to the step handler

## State Transitions

WriteToExcelStep has no internal state. The ExcelWriter is stateless (open-write-save-close per call).

The step execution flow:
1. Handler receives (step, session, row_data)
2. Determines value based on write_mode: "x" for mark_done, clipboard content for paste_clipboard
3. Computes Excel row = session.current_row + 1 (header offset)
4. Calls ExcelWriter.write_cell(file_path, sheet_name, row, column_name, value)
5. Returns (handler continues to next step)
