# Research: Screen Loaded Step

## Decision 1: Handler Retry Loop Implementation

**Decision**: Implement the retry loop directly in the step handler registered in `main.py`. The handler will loop up to `max_tries`, performing clear → drag → copy → check on each iteration, with a 1-second interruptible sleep between attempts.

**Rationale**: The handler already has access to all needed modules (clipboard, mouse, keyboard) and the session/kill-switch. No new module or abstraction is needed — the loop is simple and self-contained. This follows Constitution III (no unnecessary abstractions).

**Alternatives considered**:
- Create a separate ScreenLoadedModule: Over-engineering for a single loop; adds a file with no reuse benefit.
- Use executor-level retry logic: Would require changing the executor's step execution model; too invasive.

## Decision 2: Clipboard Check — Empty vs Whitespace

**Decision**: Treat clipboard content as "empty" if it is an empty string or contains only whitespace characters. Use `clipboard_text.strip()` to normalize.

**Rationale**: When dragging over a region with no text, the clipboard may contain whitespace characters (spaces, newlines) from the selection. These should not count as "screen loaded" — the user expects visible text content.

**Alternatives considered**:
- Check only for empty string: Would miss whitespace-only selections, causing false positives.
- Check for minimum character count: Over-constraining; any non-whitespace character indicates the screen has content.

## Decision 3: Interruptible Sleep During Retries

**Decision**: Use the existing `WaitModule.interruptible_sleep()` with the kill-switch event for the 1-second wait between retries. If the kill-switch is triggered during the wait, the handler breaks out of the loop and stops the session.

**Rationale**: The executor already uses this pattern for WAIT steps and step delays. Reusing it ensures consistent kill-switch behavior across all wait scenarios.

**Alternatives considered**:
- Use `time.sleep(1)`: Would block the kill-switch for 1 second per retry; violates Constitution I (Safety First).
- Use `kill_switch.wait_for_trigger(timeout=1.0)`: Also viable, but `interruptible_sleep` is the established pattern in the codebase.

## Decision 4: Workflow Stop on Max Tries Exceeded

**Decision**: When max tries is exceeded, the handler calls `session.stop()` to halt the workflow. The executor's existing loop checks `session.status` between steps and will break out naturally.

**Rationale**: This is the same mechanism used by the kill-switch. The executor already handles `session.status != "running"` gracefully, logging a "Stopped at row X" message.

**Alternatives considered**:
- Raise an exception: Would trigger the executor's error handling path instead of a clean stop; less user-friendly.
- Return a failure flag: Would require changing the handler signature; breaks existing pattern.

## Decision 5: Drag + Copy Sequence Timing

**Decision**: Use the existing `mouse.drag()` method (mouseDown → moveTo with 0.5s duration → mouseUp) followed by a 50ms delay, then `pyautogui.hotkey('ctrl', 'c')` with a 50ms delay for the copy to complete before checking clipboard.

**Rationale**: The drag method already exists and works reliably. The 50ms delays match the existing Copy Field step pattern (clear → select all → copy with 50ms gaps). This ensures the OS has time to process the clipboard update.

**Alternatives considered**:
- Shorter delays: Risk clipboard not being updated in time on slower systems.
- Longer delays: Unnecessary; 50ms is proven sufficient in the Copy Field step.
