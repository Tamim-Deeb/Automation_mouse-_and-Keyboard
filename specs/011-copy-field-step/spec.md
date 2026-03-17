# Feature Specification: Copy Field Step

**Feature Branch**: `011-copy-field-step`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "add a step to the steps named copy field, which will clean the clipboard, then ctrl+a then ctrl+c"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Copy Field Step Type (Priority: P1)

The user needs to capture the full contents of a focused input field during workflow execution. Instead of manually adding three separate steps (clear clipboard, Ctrl+A, Ctrl+C), the user adds a single "Copy Field" step from the step type dropdown. When executed, this step automatically performs the three actions in sequence: clears the system clipboard, selects all text in the currently focused field (Ctrl+A), and copies it to the clipboard (Ctrl+C). The copied value is then available for subsequent workflow steps or for the user's own use.

**Why this priority**: This is the entire feature — a single composite step that replaces a tedious 3-step manual workflow. It's the minimum viable addition.

**Independent Test**: Add a "Copy Field" step to a workflow, focus a text field with known content, run the workflow, and verify the clipboard contains exactly the field's text.

**Acceptance Scenarios**:

1. **Given** a workflow with a "Copy Field" step and a text field focused with content "Hello World", **When** the step executes, **Then** the clipboard contains "Hello World"
2. **Given** a workflow with a "Copy Field" step and an empty focused field, **When** the step executes, **Then** the clipboard is empty (cleared)
3. **Given** the clipboard contains stale data from a previous operation, **When** a "Copy Field" step executes, **Then** the stale data is replaced by the current field contents (clipboard was cleared before copy)
4. **Given** a "Copy Field" step in a workflow, **When** the user views the workflow steps board, **Then** the step displays as "Copy Field" (no additional parameters needed)

---

### Edge Cases

- What happens if no field is focused when the step executes? The step still runs (Ctrl+A and Ctrl+C are sent to whatever has focus), and the clipboard may contain unexpected content. This is the same behavior as manually pressing those keys — the user is responsible for ensuring focus is correct via prior click steps.
- What happens during dry-run mode? The step is logged but not executed, consistent with all other step types.
- What happens if the kill switch (Esc) is pressed during the step? Since the step is very fast (three near-instant operations), it will complete the current sub-action and stop at the next kill-switch check between steps.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Copy Field" step type in the workflow step type dropdown
- **FR-002**: When executed, the "Copy Field" step MUST perform three actions in sequence: (1) clear the system clipboard, (2) select all (Ctrl+A), (3) copy (Ctrl+C)
- **FR-003**: The "Copy Field" step MUST require no user-configurable parameters — it is a zero-parameter step
- **FR-004**: The "Copy Field" step MUST be logged in the action log with a descriptive message, consistent with other step types
- **FR-005**: The "Copy Field" step MUST be saveable and loadable as part of workflow serialization
- **FR-006**: A brief delay MUST be inserted between each sub-action (clear, select all, copy) to allow the operating system to process each operation

### Key Entities

- **Copy Field Step**: A workflow step type that performs a composite action — clearing the clipboard, selecting all text in the focused field, and copying it. No parameters. Represented as a single step in the workflow builder.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add and execute a "Copy Field" step in under 5 seconds (single step instead of three)
- **SC-002**: After executing a "Copy Field" step, the clipboard contains the exact text from the focused field in 100% of executions
- **SC-003**: Workflows containing "Copy Field" steps save and load correctly across application restarts

## Assumptions

- The clipboard is cleared before Ctrl+A/Ctrl+C to ensure stale data doesn't persist if the copy fails (e.g., empty field).
- A small delay (50-100ms) between sub-actions is sufficient for the OS to process clipboard and selection operations.
- The step does not need any parameters because it always operates on the currently focused field.
- The step type integrates with the existing step registry and serialization system without changes to those systems.
