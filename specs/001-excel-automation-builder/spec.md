# Feature Specification: Excel-Driven Desktop Automation Workflow Builder

**Feature Branch**: `001-excel-automation-builder`
**Created**: 2026-03-09
**Status**: Draft
**Input**: User description: "Build a desktop application that allows non-technical users to create, save, load, and execute reusable desktop automation workflows driven by Excel data row-by-row."

## Clarifications

### Session 2026-03-09

- Q: How does the user specify screen coordinates for click steps? → A: Both click-to-capture (primary) and manual X/Y entry for fine-tuning.
- Q: How should "insert column value" deliver text to the target application? → A: Type character-by-character via simulated keystrokes (universally compatible, no clipboard side effects).
- Q: Can the user select a starting row for execution? → A: Yes, user can set a start row before execution to enable resuming after interruptions.
- Q: What is the maximum worksheet size the system must handle reliably? → A: Up to 10,000 rows.
- Q: What should happen when an "insert column value" step encounters a numeric or date value? → A: Always use the cell's displayed/formatted text as shown in Excel.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build and Run a Basic Workflow (Priority: P1)

A data-entry operator opens the application, imports an Excel workbook, and selects a worksheet. They build a workflow by adding steps: click at coordinates (100, 200), insert the value from column "Name", press Tab, insert the value from column "Email", and press Enter. They start execution. The system processes each row in the worksheet, performing the defined steps for every row. The operator watches the progress and the automation completes all rows.

**Why this priority**: This is the core value proposition — without row-by-row execution of a user-defined step sequence, the product delivers zero value.

**Independent Test**: Can be fully tested by creating a 5-row Excel file with two columns, building a workflow with click + insert + hotkey steps, and verifying that all 5 rows are processed with correct column values inserted at the right steps.

**Acceptance Scenarios**:

1. **Given** the user has imported a workbook and selected a worksheet with 10 rows, **When** they build a workflow with click, insert-column, and hotkey steps and press Start, **Then** the system executes the step sequence once per row from first to last row.
2. **Given** a workflow uses "insert value from column B" and "insert value from column D" steps, **When** the workflow runs on row 3, **Then** the system inserts the actual values from columns B and D of row 3.
3. **Given** a workflow includes a "wait 500ms" step between two click steps, **When** execution reaches that step, **Then** the system pauses for approximately 500ms before continuing.

---

### User Story 2 - Save and Reload a Workflow (Priority: P2)

An office worker has spent time building a workflow with 12 steps. They save the workflow to a file. The next day, they open the application, load the saved workflow, and see all 12 steps restored exactly as configured. They attach a new Excel file and run the workflow again.

**Why this priority**: Without persistence, users must rebuild workflows from scratch every session, making the tool impractical for daily use.

**Independent Test**: Can be tested by building a workflow with every supported step type, saving it, closing the application, reopening, loading the file, and verifying every step and its parameters match the original.

**Acceptance Scenarios**:

1. **Given** a workflow with steps including click (150, 300), double-click (200, 400), type "hello", wait 1000ms, insert column "ID", and press Ctrl+V, **When** the user saves and reloads it, **Then** every step type and parameter is identical to the original.
2. **Given** a user loads a saved workflow, **When** they attach a different Excel file with the same column names, **Then** the workflow executes correctly against the new data.

---

### User Story 3 - Stop Execution Safely (Priority: P2)

An operator starts a workflow on a 500-row spreadsheet. After 50 rows, they notice the target application has changed its layout. They press the stop button (or the Esc hotkey). Execution halts immediately after completing the current step. No further rows are processed.

**Why this priority**: Automation without a reliable abort mechanism is dangerous — it can cause data corruption or unintended actions in external applications.

**Independent Test**: Can be tested by running a workflow on a large dataset and triggering stop mid-execution, then verifying that no actions occur after the stop signal.

**Acceptance Scenarios**:

1. **Given** a workflow is executing on row 50 of 500, **When** the user presses the Stop button, **Then** execution halts after the current step completes and no further rows are processed.
2. **Given** a workflow is executing, **When** the user presses the Esc key, **Then** execution halts with the same behavior as the Stop button.
3. **Given** execution has been stopped, **When** the user inspects the application, **Then** a message indicates which row was the last to be processed.

---

### User Story 4 - Manage Workflow Steps (Priority: P3)

A user builds a workflow and realizes they need to reorder steps, delete an incorrect step, and add a new step in the middle. They drag a step to a new position, delete another step, and insert a new "type text" step between two existing steps. The workflow reflects all changes immediately in the step list.

**Why this priority**: Editing flexibility is essential for usability, but a workflow can still be rebuilt from scratch without it.

**Independent Test**: Can be tested by creating a 5-step workflow, reordering step 3 to position 1, deleting step 4, adding a new step at position 2, and verifying the final order matches expectations.

**Acceptance Scenarios**:

1. **Given** a workflow with steps [A, B, C, D], **When** the user moves step C to position 1, **Then** the step list shows [C, A, B, D].
2. **Given** a workflow with steps [A, B, C], **When** the user deletes step B, **Then** the step list shows [A, C].
3. **Given** a workflow with steps [A, B], **When** the user adds a new step between A and B, **Then** the step list shows [A, New, B].

---

### Edge Cases

- What happens when an Excel cell referenced by an "insert column value" step is empty? The system inserts an empty string and continues execution (no error).
- What happens when the selected worksheet has zero data rows (only headers)? The system displays a warning message and does not start execution.
- What happens when the user saves a workflow but the file path is not writable? The system displays an error message and does not lose the in-memory workflow.
- What happens when the user loads a workflow file that is corrupted or in an unsupported format? The system displays an error message and leaves the current workflow unchanged.
- What happens when the Excel file has columns with duplicate names? The system uses the first occurrence of the column name and warns the user.
- What happens when screen coordinates in a click step are outside the current screen bounds? The system skips the step, logs a warning, and continues to the next step.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to import an Excel workbook (.xlsx) and select one worksheet from it.
- **FR-002**: System MUST execute a workflow by iterating through each data row of the selected worksheet, running all workflow steps per row. The user MUST be able to set a starting row number before execution (default: first data row) to enable resuming after interruptions.
- **FR-003**: System MUST treat the first row of the worksheet as column headers (not data).
- **FR-004**: Users MUST be able to add workflow steps from these types: single click, double click, type text, wait, insert column value, press hotkey.
- **FR-005**: For click and double-click steps, the user MUST specify screen X and Y coordinates. The system MUST provide a click-to-capture mode (user clicks a "pick" button, then clicks the screen target to record coordinates) as the primary input method, and MUST also allow manual entry of X/Y values for fine-tuning.
- **FR-006**: For "type text" steps, the user MUST specify the literal text string to type.
- **FR-007**: For "wait" steps, the user MUST specify the duration in milliseconds.
- **FR-008**: For "insert column value" steps, the user MUST select a column name from the imported worksheet's headers. The system MUST deliver the value by typing it character-by-character via simulated keystrokes (not clipboard paste). The system MUST use the cell's displayed/formatted text (not the raw underlying value), so dates and numbers appear exactly as shown in Excel.
- **FR-009**: For "press hotkey" steps, the user MUST select from a predefined list: Enter, Backspace, Tab, Shift+Tab, Ctrl+A, Ctrl+C, Ctrl+V. (Note: Esc is reserved as the kill-switch hotkey and cannot be used as a workflow step.)
- **FR-010**: A single workflow MUST support multiple "insert column value" steps referencing different columns within the same row iteration.
- **FR-011**: Users MUST be able to reorder workflow steps via the interface.
- **FR-012**: Users MUST be able to delete any workflow step.
- **FR-013**: Users MUST be able to save a workflow to a file and load it back with all steps and parameters preserved.
- **FR-014**: Users MUST be able to start workflow execution with a single action (button click).
- **FR-015**: Users MUST be able to stop workflow execution at any time; the system MUST halt after completing the current step.
- **FR-016**: The system MUST register a kill-switch hotkey (default: Esc) that stops execution after the current step completes.
- **FR-017**: The system MUST display execution progress showing the current row number and total rows.
- **FR-018**: The system MUST log every action performed during execution with timestamps.
- **FR-019**: The system MUST support a dry-run mode that logs all intended actions without sending any mouse or keyboard events to the operating system. (Constitution requirement: Safety & Operational Constraints.)

### Key Entities

- **Workflow**: A named, ordered sequence of steps. Can be saved to and loaded from a file. Associated with an Excel file and worksheet at execution time.
- **Workflow Step**: A single action within a workflow. Has a type (click, double-click, type-text, wait, insert-column-value, press-hotkey) and type-specific parameters (coordinates, text, duration, column name, hotkey).
- **Excel Data Source**: A workbook file with a selected worksheet. Provides column headers for step configuration and row data for execution. MUST support worksheets up to 10,000 rows.
- **Execution Session**: A single run of a workflow against a data source. Tracks current row, status (running/stopped/completed), and produces an action log.

## Assumptions

- The target desktop applications are already open and positioned before the user starts automation. The system does not launch or arrange external applications.
- Column headers in the Excel file are unique and located in the first row.
- The user has sufficient screen resolution and does not change display settings during execution.
- Workflow files are stored locally on the user's machine.
- A configurable default delay (minimum 50ms) is applied between steps to account for UI rendering in target applications.

## Out of Scope

- OCR or image-based screen element targeting
- Conditional logic or branching within workflows
- Nested loops beyond the per-row execution model
- End-user scripting or code editing
- Cloud storage, sharing, or multi-user features
- Scheduling or unattended execution
- Support for file formats other than .xlsx

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A non-technical user can build and execute a 5-step workflow within 5 minutes of first opening the application.
- **SC-002**: A saved workflow reloads with 100% fidelity — every step type, parameter, and order matches the original.
- **SC-003**: The system processes worksheets up to 10,000 rows without skipping any rows or steps and without excessive memory consumption.
- **SC-004**: Execution stops within 2 seconds of the user pressing Stop or the kill-switch hotkey.
- **SC-005**: A workflow using 3 or more different column values from the same row correctly inserts the right value at each step.
- **SC-006**: 90% of first-time users (non-technical) can configure and run a basic workflow without external help or documentation.
