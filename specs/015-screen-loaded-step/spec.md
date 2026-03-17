# Feature Specification: Screen Loaded Step

**Feature Branch**: `015-screen-loaded-step`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "add a new step named screen loaded, it's a simple step which will check the screen if loaded by emptying the clipboard and press and drag on the screen from start coords to end coords like the click and move step, the user will choose the two coords of course, and it will copy the text since the user's coords describe the beginning and end of a word, if the clipboard after copying not empty the workflow will continue, if it's empty it will wait for 1 sec and try to copy again, the max tries also the user will determine, if it exceeds the max tries, the workflow will stop"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Wait for Screen Content to Load (Priority: P1)

As a user automating a workflow that navigates between screens or pages, I want a "Screen Loaded" step that waits until specific text appears on screen before continuing, so the workflow doesn't proceed before the target application is ready.

The step works by:
1. Clearing the clipboard
2. Clicking and dragging from start coordinates to end coordinates (selecting a word/text region the user specified)
3. Copying the selected text (Ctrl+C)
4. Checking if the clipboard has content — if yes, the screen is loaded and the workflow continues
5. If the clipboard is empty, waiting 1 second and retrying
6. Repeating up to a user-configured maximum number of attempts
7. If max attempts are exceeded, stopping the entire workflow

**Why this priority**: This is the core and only functionality of the feature — without it, there is no value delivered.

**Independent Test**: Can be fully tested by adding a Screen Loaded step with start/end coordinates pointing to known text on screen, setting max tries to 3, running the workflow, and verifying the workflow continues when text is present or stops after max retries when text is absent.

**Acceptance Scenarios**:

1. **Given** a workflow with a Screen Loaded step configured with start coords (100, 200), end coords (300, 200), and max tries 5, **When** the target text is already visible on screen at those coordinates, **Then** the step succeeds on the first attempt and the workflow continues to the next step.
2. **Given** a Screen Loaded step with max tries 3, **When** the target text appears after 2 seconds (2 retries), **Then** the step succeeds on the 3rd attempt and the workflow continues.
3. **Given** a Screen Loaded step with max tries 3, **When** the target text never appears, **Then** the step fails after 3 attempts (each with a 1-second wait) and the entire workflow stops with a status message indicating the screen did not load.
4. **Given** a workflow with a Screen Loaded step, **When** the user opens the step editor, **Then** they see start/end coordinate fields with Pick buttons (like Click And Move), and a max tries input field.

---

### Edge Cases

- What happens if the user sets max tries to 0 or a negative number? The editor enforces a minimum of 1 attempt.
- What happens if the selected region contains only whitespace? Whitespace-only clipboard content is treated as empty (screen not loaded).
- What happens if the kill-switch is triggered during a retry wait? The step respects the kill-switch and stops immediately.
- What happens if no coordinates are configured? The editor validates that all coordinate fields are filled before saving.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Screen Loaded" step type in the Add Step dialog.
- **FR-002**: The step editor MUST show start and end coordinate fields with Pick buttons (same pattern as Click And Move step).
- **FR-003**: The step editor MUST show a "Max Tries" input field with a default value of 10 and a minimum of 1.
- **FR-004**: When executed, the step MUST clear the clipboard before each attempt.
- **FR-005**: The step MUST select text by clicking and dragging from the start coordinates to the end coordinates.
- **FR-006**: After dragging, the step MUST copy the selected text (Ctrl+C).
- **FR-007**: If the clipboard contains non-empty, non-whitespace text after copying, the step MUST succeed and the workflow MUST continue to the next step.
- **FR-008**: If the clipboard is empty or contains only whitespace, the step MUST wait 1 second and retry the entire sequence (clear, drag, copy, check).
- **FR-009**: If the number of attempts exceeds the configured max tries, the step MUST stop the entire workflow execution.
- **FR-010**: The step MUST display in the workflow list with its coordinates and max tries (e.g., "Screen Loaded (100, 200) → (300, 200) [max: 5]").
- **FR-011**: The step parameters MUST be serializable for workflow save/load.
- **FR-012**: The step MUST respect the kill-switch during retry waits — if triggered, the workflow stops immediately.

### Key Entities

- **ScreenLoadedStep**: A workflow step with parameters: start_x, start_y (int), end_x, end_y (int), max_tries (int, minimum 1, default 10).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add and configure a Screen Loaded step in under 30 seconds using the familiar coordinate picker interface.
- **SC-002**: When text is present at the target coordinates, the step succeeds on the first attempt and adds less than 500ms of overhead to the workflow.
- **SC-003**: When text is absent, the step retries at 1-second intervals up to the configured max tries, then stops the workflow with a clear status message.
- **SC-004**: Workflow save/load correctly preserves all Screen Loaded step parameters (coordinates and max tries).

## Assumptions

- The text the user targets with the coordinates is visible and selectable via mouse drag + Ctrl+C in the target application.
- A 1-second wait between retries is sufficient for most screen loading scenarios.
- The default of 10 max tries (10 seconds total wait) covers the majority of loading cases.
- The kill-switch (Esc key) remains functional during retry waits.
