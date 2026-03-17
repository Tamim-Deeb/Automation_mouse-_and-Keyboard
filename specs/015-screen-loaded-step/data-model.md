# Data Model: Screen Loaded Step

## Entities

### ScreenLoadedStep (extends WorkflowStep)

A workflow step that verifies screen content is loaded by selecting and copying text, retrying until successful or max tries exceeded.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| type | StepType | Always `SCREEN_LOADED` | Must equal StepType.SCREEN_LOADED |
| order | int | Position in workflow | Non-negative integer |
| params.start_x | int | X coordinate of drag start | Required integer |
| params.start_y | int | Y coordinate of drag start | Required integer |
| params.end_x | int | X coordinate of drag end | Required integer |
| params.end_y | int | Y coordinate of drag end | Required integer |
| params.max_tries | int | Maximum number of attempts | Required integer, minimum 1, default 10 |

## Relationships

- **ScreenLoadedStep** → uses **MouseAutomation.drag()** to select text region
- **ScreenLoadedStep** → uses **ClipboardModule.clear()** and **ClipboardModule.paste()** to manage clipboard
- **ScreenLoadedStep** → uses **pyautogui.hotkey('ctrl', 'c')** to copy selected text
- **ScreenLoadedStep** → uses **WaitModule.interruptible_sleep()** for retry waits (kill-switch aware)
- **ScreenLoadedStep** → calls **session.stop()** on max tries exceeded

## State Transitions

The step execution flow per attempt:
1. Clear clipboard
2. Wait 50ms
3. Drag from (start_x, start_y) to (end_x, end_y) — selects text
4. Wait 50ms
5. Press Ctrl+C — copies selection
6. Wait 50ms
7. Read clipboard content
8. If content is non-empty and non-whitespace → SUCCESS, continue workflow
9. If empty/whitespace and attempts < max_tries → wait 1 second (interruptible), go to step 1
10. If empty/whitespace and attempts >= max_tries → FAIL, stop workflow
