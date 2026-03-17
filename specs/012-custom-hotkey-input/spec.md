# Feature Specification: Custom Hotkey Input

**Feature Branch**: `012-custom-hotkey-input`
**Created**: 2026-03-17
**Status**: Draft
**Input**: User description: "inside the hotkey function, add an additional two box if the user wanted to use something different like ctr + f1 or shift with something, the user has to write it in this case"

## User Scenarios & Testing

### User Story 1 - Custom Hotkey via Freeform Input (Priority: P1)

As a user, I want to type a custom hotkey combination (e.g., Ctrl+F1, Shift+Home, Alt+Tab, Ctrl+Shift+F1) when the predefined dropdown options don't cover my needs. The Press Hotkey step editor should show two text input boxes for a modifier key and a main key, in addition to the existing dropdown. The modifier box accepts multiple modifiers separated by "+" (e.g., "ctrl+shift"). The user can either select from the dropdown OR type a custom combination in the input boxes.

**Why this priority**: The predefined hotkey list is limited (Escape, Enter, Backspace, Tab, Shift+Tab, Ctrl+A, Ctrl+C, Ctrl+V). Users automating real workflows need arbitrary key combinations like Ctrl+F1, Shift+End, Alt+F4, etc. Without this, the tool cannot automate workflows that require non-standard hotkeys.

**Independent Test**: Add a Press Hotkey step, ignore the dropdown, type "Ctrl" in the modifier box and "F1" in the key box, save the step, run the workflow on a focused application, and verify that Ctrl+F1 is pressed.

**Acceptance Scenarios**:

1. **Given** the user is adding a Press Hotkey step, **When** they open the step editor, **Then** they see the existing hotkey dropdown AND two additional text input boxes labeled "Modifier (optional)" and "Key" below it
2. **Given** the user has typed "Ctrl" in the modifier box and "F1" in the key box, **When** they click Save, **Then** the step is saved with the custom hotkey "ctrl+f1"
3. **Given** the user has selected a hotkey from the dropdown AND also filled in the custom input boxes, **When** they click Save, **Then** the custom input boxes take priority over the dropdown selection
4. **Given** the user has typed only a key (e.g., "F5") with no modifier, **When** they click Save, **Then** the step is saved with just "f5" as a single key press
5. **Given** a workflow is loaded that contains a custom hotkey step (e.g., "ctrl+f1"), **When** the step is displayed in the workflow list, **Then** it shows "Press Hotkey: ctrl+f1"
6. **Given** a custom hotkey step is executed, **When** the workflow runs, **Then** the system presses the exact key combination specified

---

### Edge Cases

- What happens when the user leaves both custom input boxes empty and no dropdown selection is made? The editor should show a validation error requiring either a dropdown selection or at least the Key box to be filled.
- What happens when the user types an invalid key name (e.g., "xyz")? The execution engine will attempt the keypress via pyautogui; if it fails, the error is logged without crashing the workflow.
- What happens when the user types modifier names with inconsistent casing (e.g., "CTRL", "ctrl", "Ctrl")? The system accepts any casing and normalizes to lowercase before execution.
- What happens when the user fills in only the Modifier box but leaves the Key box empty? The editor shows a validation error — a modifier alone is not a valid hotkey.

## Requirements

### Functional Requirements

- **FR-001**: The Press Hotkey step editor MUST display two text input boxes labeled "Modifier (optional)" and "Key" below the existing hotkey dropdown
- **FR-002**: The user MUST be able to save a step using either the dropdown selection OR the custom input boxes
- **FR-003**: If the Key input box has content, the custom input MUST take priority over the dropdown selection
- **FR-004**: The Key input box MUST be required when using custom input (modifier is optional)
- **FR-005**: The system MUST normalize custom key names to lowercase before storing and executing
- **FR-006**: Custom hotkey steps MUST be serialized as a string in the format "modifier+key" (e.g., "ctrl+f1") or just "key" (e.g., "f5") when no modifier is provided
- **FR-007**: The workflow list display MUST show custom hotkeys in their stored form (e.g., "Press Hotkey: ctrl+f1")
- **FR-008**: The execution handler MUST support executing custom hotkey strings by parsing the "+" separator and pressing the keys via the automation layer
- **FR-009**: Custom hotkey values MUST be saved and loaded correctly via the existing workflow serializer (JSON)
- **FR-010**: All existing predefined hotkey functionality MUST continue to work unchanged

### Key Entities

- **Custom Hotkey**: A user-defined key combination stored as a string (e.g., "ctrl+f1", "ctrl+shift+f1", "shift+end", "f5"). Consists of optional modifier(s) and a required key, joined by "+". The modifier box accepts multiple modifiers (e.g., "ctrl+shift").

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can define and execute any key combination supported by the underlying automation system, beyond the predefined 8 hotkeys
- **SC-002**: Custom hotkey steps can be saved to JSON and reloaded without data loss
- **SC-003**: 100% of existing predefined hotkey functionality continues to work unchanged
- **SC-004**: Users can complete the custom hotkey configuration in under 30 seconds

## Clarifications

### Session 2026-03-17

- Q: Should the custom hotkey support multiple modifiers (e.g., Ctrl+Shift+F1)? → A: Yes, the single modifier box accepts multiple modifiers separated by "+" (e.g., user types "ctrl+shift" in the modifier box)

## Assumptions

- pyautogui supports the key names the user will type (e.g., "f1", "home", "end", "pageup", etc.)
- Users are expected to know valid key names; no exhaustive validation is performed at save time
- The existing hotkey dropdown remains for convenience — it is not removed or modified
