# Feature Specification: Safe Stop (Esc Key Kill Switch)

**Feature Branch**: `009-safe-stop`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "make a safe stop which force the loop to stop after clicking esc"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Emergency Stop During Execution (Priority: P1)

A user starts a workflow that iterates over many Excel rows, performing mouse clicks and keyboard input. Midway through, they realize something is wrong (wrong target window, incorrect data, etc.) and need to stop the automation immediately. They press the Esc key and the workflow stops within one second, regardless of what step is currently executing.

**Why this priority**: This is the core safety mechanism. Without a reliable emergency stop, the automation tool can cause unintended damage — clicking the wrong buttons, typing in the wrong fields, or running indefinitely. This is the single most critical user need for this feature.

**Independent Test**: Can be fully tested by starting any multi-row workflow, pressing Esc during execution, and verifying the workflow halts promptly. Delivers immediate safety value.

**Acceptance Scenarios**:

1. **Given** a workflow is running and processing row 5 of 100, **When** the user presses Esc, **Then** the workflow stops before the next step begins, the UI shows "Stopped at row 5 of 100", and the Start button becomes available again.
2. **Given** a workflow is running and the application window is minimized or unfocused, **When** the user presses Esc, **Then** the workflow still stops because the kill switch listens globally.
3. **Given** a workflow is running a long wait step (e.g., 5 seconds), **When** the user presses Esc during the wait, **Then** the wait is interrupted and the workflow stops without waiting for the full duration.

---

### User Story 2 - Visual Feedback on Safe Stop (Priority: P2)

When the user triggers the safe stop, they receive clear visual confirmation that the workflow has been stopped, including which row it stopped on. This gives the user confidence that the stop was successful and helps them resume from the correct position later.

**Why this priority**: Without feedback, the user cannot tell if the stop worked or where execution halted. Important for usability but the core stop mechanism (P1) must work first.

**Independent Test**: Can be tested by triggering Esc during execution and verifying the status label, progress indicator, and completion dialog all reflect the stopped state accurately.

**Acceptance Scenarios**:

1. **Given** a workflow is stopped via Esc, **When** the stop completes, **Then** the status label shows the row where execution stopped, the Start button is re-enabled, and the Stop button is disabled.
2. **Given** a workflow is stopped via Esc, **When** the completion dialog appears, **Then** it indicates the workflow was stopped by the user (not an error) and shows the log file location.

---

### Edge Cases

- What happens if the user presses Esc when no workflow is running? Nothing should happen — the application should ignore it.
- What happens if the user presses Esc multiple times rapidly during execution? The first press should trigger the stop; subsequent presses should be harmless.
- What happens if the workflow is on its very last step of the very last row when Esc is pressed? The workflow should still stop gracefully and report the stopped state rather than completing.
- What happens if a step handler is in the middle of a pyautogui action (e.g., mid-typing) when Esc is pressed? The current atomic action (single click, single keystroke) may complete, but no further actions should execute.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST stop workflow execution within 1 second of the user pressing the Esc key.
- **FR-002**: System MUST check for the kill switch signal between every workflow step within a row, not just between rows.
- **FR-003**: System MUST interrupt long wait steps when the kill switch is triggered, rather than waiting for the full duration to elapse.
- **FR-004**: The Esc key kill switch MUST work globally — even when the application window is minimized, unfocused, or behind other windows.
- **FR-005**: System MUST update the UI to reflect the stopped state after the kill switch is triggered (re-enable Start button, disable Stop button, show stopped row).
- **FR-006**: System MUST cleanly release the global keyboard listener after execution ends (whether by completion, stop button, or Esc key).
- **FR-007**: The kill switch MUST NOT interfere with normal Esc key usage when no workflow is running.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Workflow execution halts within 1 second of pressing Esc in 100% of test scenarios.
- **SC-002**: The stopped row number displayed matches the actual last row processed, with no off-by-one errors.
- **SC-003**: After stopping, the user can successfully start a new execution without restarting the application.
- **SC-004**: The Esc key triggers a stop even when the application window is not focused, on both macOS and Windows.

## Assumptions

- The existing `KillSwitch` class provides the global Esc key listener via pynput. The core issue is that its `is_triggered()` state is not checked by the executor during the row/step loop — the kill switch event needs to be wired into the executor's control flow.
- A single atomic pyautogui action (one click, one keystroke) is allowed to complete before stopping. The system does not need to interrupt mid-keystroke.
- The pynput keyboard listener works reliably on both macOS and Windows for this use case (keyboard-only listener, no mouse listener).
