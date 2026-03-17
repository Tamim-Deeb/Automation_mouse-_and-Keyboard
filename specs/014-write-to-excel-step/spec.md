# Feature Specification: Write To Excel Step

**Feature Branch**: `014-write-to-excel-step`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "make a new step to write back to excel to the same sheet same line but the user can choose the column, two options to write, mark done (x), or paste the clipboard"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mark Done in Excel (Priority: P1)

As a user building an automation workflow, I want a "Write To Excel" step that writes a fixed "x" value into a chosen column on the same row currently being processed, so I can mark rows as completed during workflow execution.

**Why this priority**: Marking rows as done is the most common write-back use case — it lets users track which rows have already been processed without leaving the application.

**Independent Test**: Can be fully tested by adding a "Write To Excel" step with "Mark Done" mode, selecting a target column, running the workflow, and verifying the Excel file contains "x" in the chosen column for each processed row.

**Acceptance Scenarios**:

1. **Given** a workflow with a Write To Excel step configured to "Mark Done" targeting column "Status", **When** the workflow executes row 3, **Then** the value "x" is written to the "Status" column of row 3 in the same Excel file and sheet.
2. **Given** a workflow with a Write To Excel step, **When** the user opens the step editor, **Then** they see a dropdown of available columns (from the loaded Excel headers) and a write mode selector with "Mark Done" and "Paste Clipboard" options.
3. **Given** a Write To Excel step configured for "Mark Done", **When** the step executes, **Then** the Excel file is saved after writing and subsequent steps can continue normally.

---

### User Story 2 - Paste Clipboard to Excel (Priority: P2)

As a user, I want a "Write To Excel" step that writes the current clipboard content into a chosen column on the same row, so I can capture data copied during earlier steps (e.g., via Copy Field) back into the spreadsheet.

**Why this priority**: Paste Clipboard extends the write-back capability by allowing dynamic content capture, enabling workflows that copy values from applications and store them in Excel.

**Independent Test**: Can be fully tested by copying text to the clipboard, running a workflow with a "Write To Excel" step in "Paste Clipboard" mode targeting a column, and verifying the clipboard text appears in the Excel cell.

**Acceptance Scenarios**:

1. **Given** a workflow with a Write To Excel step configured to "Paste Clipboard" targeting column "Result", and the clipboard contains "Hello World", **When** the workflow executes row 5, **Then** "Hello World" is written to the "Result" column of row 5.
2. **Given** the clipboard is empty when a "Paste Clipboard" Write To Excel step executes, **Then** an empty string is written to the target cell (no error).

---

### Edge Cases

- What happens when the Excel file is locked by another process? The step should report an error in the execution log and continue to the next step.
- What happens if no Excel file is loaded when adding this step? The column dropdown should be empty, and the user should not be able to save without selecting a column.
- What happens when multiple Write To Excel steps target the same cell in one row? Each write overwrites the previous value — last write wins.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Write To Excel" step type in the Add Step dialog.
- **FR-002**: The step editor MUST show a dropdown of available columns populated from the loaded Excel headers.
- **FR-003**: The step editor MUST show a write mode selector with two options: "Mark Done (x)" and "Paste Clipboard".
- **FR-004**: When write mode is "Mark Done", the step handler MUST write the string "x" to the target column of the current row.
- **FR-005**: When write mode is "Paste Clipboard", the step handler MUST read the current system clipboard content and write it to the target column of the current row.
- **FR-006**: The step MUST write to the same Excel file and sheet that was loaded as the data source.
- **FR-007**: The step MUST save the Excel file after writing to ensure data is persisted.
- **FR-008**: The step MUST appear in the workflow list display with its write mode and target column (e.g., "Write To Excel [Status] (Mark Done)").
- **FR-009**: The step parameters MUST be serializable for workflow save/load.
- **FR-010**: The step MUST NOT interfere with the existing read-only Excel reading during row iteration — writing must use a separate write mechanism.

### Key Entities

- **WriteToExcelStep**: A workflow step with parameters: target column name (string), write mode ("mark_done" or "paste_clipboard").
- **ExcelWriter**: A module responsible for opening the Excel file in write mode, updating a specific cell, and saving the file.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a Write To Excel step, configure column and mode, and execute it within the existing workflow in under 30 seconds.
- **SC-002**: After workflow execution, the Excel file contains the correct values in the target column for all processed rows.
- **SC-003**: Workflow save/load correctly preserves Write To Excel step configuration (column and mode).
- **SC-004**: Write To Excel step integrates seamlessly with existing steps — users can place it anywhere in the step sequence.

## Assumptions

- The Excel file is not open in another application during workflow execution (openpyxl cannot write to files locked by Excel).
- The clipboard module (pyperclip or similar) is already available in the project for the Paste Clipboard mode.
- Writing to Excel happens synchronously during step execution — no background/async write is needed.
- The executor provides enough context (file path, sheet name, current row number) to the step handler for writing.
