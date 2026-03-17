# Feature Specification: Default Step Delay

**Feature Branch**: `010-default-step-delay`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "after each step there should be a default wait, which is not in the workflow steps board but the user can modify it before running the loop"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurable Default Delay Between Steps (Priority: P1)

The user builds a workflow with multiple steps (clicks, typing, hotkeys, etc.) and wants a consistent pause between each step to give the target application time to respond. Instead of manually adding WAIT steps between every action in the workflow builder, the user sets a single "Delay between steps" value in the execution panel before clicking Start. During execution, this delay is automatically inserted after each step without appearing in the workflow steps list.

**Why this priority**: This is the core feature — without it, users must manually add WAIT steps between every action, which is tedious and clutters the workflow. A global delay setting dramatically simplifies workflow creation for the most common use case.

**Independent Test**: Create a workflow with 3+ steps (e.g., click, type, click). Set the delay to 1000ms. Run the workflow and observe that there is a ~1 second pause between each step execution.

**Acceptance Scenarios**:

1. **Given** a workflow with 3 steps and default delay set to 500ms, **When** the user starts execution, **Then** a 500ms pause occurs after each step before the next step begins
2. **Given** a workflow with steps and default delay set to 0ms, **When** the user starts execution, **Then** steps execute back-to-back with no artificial delay
3. **Given** a workflow that also contains explicit WAIT steps, **When** the user starts execution with a default delay of 300ms, **Then** both the explicit WAIT step duration and the 300ms default delay are applied (the default delay still occurs after the WAIT step completes)

---

### User Story 2 - Delay Value Persistence Across Sessions (Priority: P2)

The user sets a preferred default delay value (e.g., 500ms) and expects it to remain when they reopen the application or switch workflows. The last-used delay value is remembered so the user doesn't have to re-enter it every time.

**Why this priority**: Quality-of-life improvement that reduces friction. Without persistence, users must re-enter their preferred delay every session, which is annoying for repeated use.

**Independent Test**: Set the delay to 750ms, close and reopen the application, verify the delay field still shows 750ms.

**Acceptance Scenarios**:

1. **Given** the user sets the default delay to 750ms and closes the application, **When** they reopen it, **Then** the delay field shows 750ms
2. **Given** the user has never set a delay, **When** they open the execution panel, **Then** the delay field shows the default value of 200ms

---

### Edge Cases

- What happens when the user enters a negative delay value? System rejects it and keeps the previous valid value.
- What happens when the user enters a non-numeric value? The input field only accepts numeric input.
- What happens when the kill switch (Esc) is pressed during a default delay pause? The delay is interruptible — execution stops immediately, consistent with existing WAIT step behavior.
- What happens during dry-run mode? The default delay is still applied so the user can observe simulated execution at realistic speed.
- What happens when the delay is set extremely high (e.g., 60000ms)? The system accepts it — the user may have a legitimate reason for a long pause.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Delay between steps" input field in the execution panel, visible alongside the existing Start Row and Dry Run controls
- **FR-002**: The delay input MUST accept values in milliseconds, with a minimum of 0ms (no delay) and a default of 200ms
- **FR-003**: During execution, the system MUST insert the configured delay after each step execution, before proceeding to the next step
- **FR-004**: The default delay MUST NOT appear as a step in the workflow steps board — it is purely an execution-time setting
- **FR-005**: The default delay pause MUST be interruptible by the kill switch (Esc key), consistent with existing WAIT step behavior
- **FR-006**: The delay input MUST only accept non-negative integer values; invalid input is rejected
- **FR-007**: The last-used delay value MUST persist across application sessions
- **FR-008**: The default delay MUST apply in both normal and dry-run execution modes

### Key Entities

- **Default Step Delay**: A user-configurable execution setting (in milliseconds) that controls the pause duration inserted between each workflow step. Not part of the workflow definition — stored as an application preference.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can set a delay value and start execution in under 5 seconds (no additional workflow editing needed)
- **SC-002**: Delay between steps is consistent (within 50ms tolerance of configured value) across all step transitions
- **SC-003**: Pressing Esc during a default delay pause stops execution within 1 second, matching existing safe-stop behavior
- **SC-004**: Delay value persists correctly across 100% of application restarts

## Assumptions

- The default delay of 200ms is a reasonable starting point for most automation scenarios — fast enough to not feel sluggish, slow enough to give target applications time to respond.
- The delay is applied uniformly after every step. Per-step delay customization is out of scope.
- The delay applies after the last step of each row as well, providing a consistent rhythm before moving to the next row.
- Persistence uses the same mechanism as any existing application preferences (or a simple local file if none exists).
