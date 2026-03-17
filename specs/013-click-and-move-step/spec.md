# Feature Specification: Click And Move Step

**Feature Branch**: `013-click-and-move-step`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "new step to the left. click and move, which is clicking on the left button on the mouse and move the mouse and release, in this case the user required to input the coords two time, the start and the end, please dont miss things up this time, pick the coords in the same way we picked it in the click step"

## User Scenarios & Testing

### User Story 1 - Click And Move (Drag) Step (Priority: P1)

As a user, I want to add a "Click And Move" step that performs a mouse drag operation: press the left mouse button at a start position, move to an end position, and release. This is useful for drag-and-drop actions, selecting text by dragging, moving sliders, resizing windows, or rearranging items.

The step editor MUST show two sets of coordinate fields — **Start (X, Y)** and **End (X, Y)** — each with its own "Pick" button that works exactly like the existing Click step's coordinate picker. The user clicks "Pick" next to the start coordinates, clicks a point on screen, and the start X/Y fields are populated. Then clicks "Pick" next to the end coordinates, clicks another point on screen, and the end X/Y fields are populated.

**Why this priority**: Drag operations are a fundamental mouse interaction that many automation workflows require (drag-and-drop, slider adjustment, text selection by dragging, etc.). Without this step type, users cannot automate any workflow that involves holding the mouse button while moving.

**Independent Test**: Add a Click And Move step, pick start coordinates on a desktop icon, pick end coordinates on a folder, run the workflow, and verify the icon is dragged into the folder.

**Acceptance Scenarios**:

1. **Given** the user is adding a step, **When** they open the step type chooser, **Then** they see "Click And Move" in the list of available step types
2. **Given** the user has selected Click And Move, **When** the step editor opens, **Then** they see four coordinate fields: Start X, Start Y, End X, End Y, with a "Pick" button for the start pair and a "Pick" button for the end pair
3. **Given** the user clicks "Pick" next to the start coordinates, **When** they click a point on screen, **Then** the Start X and Start Y fields are populated with the clicked coordinates (same behavior as the Click step's picker)
4. **Given** the user clicks "Pick" next to the end coordinates, **When** they click a point on screen, **Then** the End X and End Y fields are populated with the clicked coordinates
5. **Given** the user has entered valid start and end coordinates and clicks Save, **When** the step is saved, **Then** the workflow list shows "Click And Move" with the start and end coordinates
6. **Given** a Click And Move step is executed, **When** the workflow runs, **Then** the system presses the left mouse button at the start coordinates, moves the mouse to the end coordinates, and releases the button
7. **Given** a workflow with a Click And Move step is saved to a file and reloaded, **When** the step is displayed, **Then** all four coordinate values are preserved

---

### Edge Cases

- What happens when start and end coordinates are identical? The system performs the drag anyway (press, move zero pixels, release) — this is valid and may be needed for certain click-hold-release interactions.
- What happens when the user leaves any of the four coordinate fields empty? The editor shows a validation error requiring all four values.
- What happens when the user enters non-numeric values in coordinate fields? The editor shows a validation error.
- What happens when coordinates are negative (multi-monitor setups)? Negative values are accepted, consistent with the existing Click step behavior.

## Requirements

### Functional Requirements

- **FR-001**: The step type chooser MUST include a "Click And Move" option in the step type list
- **FR-002**: The Click And Move step editor MUST display two groups of coordinate fields: "Start" (X, Y) and "End" (X, Y)
- **FR-003**: Each coordinate group MUST have its own "Pick" button that launches the coordinate picker (same picker used by the Click step)
- **FR-004**: The coordinate picker for each group MUST populate only that group's X and Y fields when a point is clicked
- **FR-005**: All four coordinate fields (start_x, start_y, end_x, end_y) MUST be required — the editor MUST show a validation error if any field is empty or non-numeric
- **FR-006**: The execution handler MUST perform a mouse drag: press left button at (start_x, start_y), move to (end_x, end_y), release
- **FR-007**: The workflow list MUST display Click And Move steps showing start and end coordinates (e.g., "Click And Move: (100, 200) → (300, 400)")
- **FR-008**: Click And Move step parameters MUST be saved and loaded correctly via the existing workflow serializer
- **FR-009**: The Click And Move step MUST pass validation when all four coordinate values are integers
- **FR-010**: All existing step types MUST continue to work unchanged

### Key Entities

- **Click And Move Step**: A drag operation defined by four integer parameters: start_x, start_y, end_x, end_y. Represents pressing the mouse at the start point, moving to the end point, and releasing.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can perform drag-and-drop operations that were previously impossible to automate with this tool
- **SC-002**: Click And Move steps can be saved to JSON and reloaded without data loss
- **SC-003**: 100% of existing step types continue to work unchanged
- **SC-004**: Users can configure a Click And Move step (pick both coordinate pairs) in under 60 seconds

## Assumptions

- The coordinate picker is reusable — it's called with a callback and populates whichever fields the callback targets
- pyautogui supports mouse drag operations (mouseDown, moveTo, mouseUp or equivalent)
- The existing `on_pick_coords` callback pattern from the Click step can be reused by passing different callbacks for start vs end coordinate groups
- Negative coordinates are accepted (multi-monitor support, consistent with Click step)
