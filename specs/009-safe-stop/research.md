# Research: Safe Stop (Esc Key Kill Switch)

**Feature Branch**: `009-safe-stop`
**Date**: 2026-03-16

## Research Tasks

### 1. How is the kill switch currently wired?

**Finding**: The `KillSwitch` class (`src/engine/kill_switch.py`) works correctly in isolation — it starts a pynput keyboard listener, and when Esc is pressed, it sets a `threading.Event`. However, the `WorkflowExecutor` (`src/engine/executor.py`) has NO reference to the kill switch. It only checks `self.session.status != "running"` in its loop. The `ExecutionPanel` creates both the kill switch and executor but never connects them.

**Decision**: Inject the `KillSwitch` instance into the `WorkflowExecutor` so the executor can check `kill_switch.is_triggered()` between steps.

**Rationale**: This is the simplest approach — no new classes, no event bus. The executor already has a check point between steps; it just needs the kill switch reference.

**Alternatives considered**:
- Polling from the GUI thread and calling `executor.stop()`: Adds latency (GUI polling is typically 100-200ms). The executor checking directly is faster and simpler.
- Using a callback from kill switch to executor: Over-engineered for a single boolean check.

### 2. How to make wait steps interruptible?

**Finding**: `WaitModule.sleep()` uses `time.sleep()` which is blocking and cannot be interrupted. The kill switch uses `threading.Event` which has a `.wait(timeout)` method that returns immediately when the event is set.

**Decision**: Add an `interruptible_sleep()` method to `WaitModule` that accepts a `threading.Event` and uses `event.wait(timeout)` instead of `time.sleep()`. This returns immediately when Esc is pressed.

**Rationale**: `threading.Event.wait(timeout)` is the standard Python pattern for interruptible waits. It sleeps for up to `timeout` seconds but wakes immediately if the event is set.

**Alternatives considered**:
- Polling `time.sleep()` in small chunks (e.g., 50ms): Works but is less clean and wastes CPU cycles on polling. `Event.wait()` is zero-overhead when waiting.

### 3. How to bridge kill switch trigger to executor stop in the GUI?

**Finding**: Even with the executor checking the kill switch directly, the GUI needs to detect when execution stops (to update buttons/labels). Currently `_on_complete` handles this, but only fires when the executor's loop finishes naturally.

**Decision**: Add a polling loop in `ExecutionPanel` that checks `kill_switch.is_triggered()` every 200ms while running. When triggered, call `executor.stop()` to set session status, which the executor also checks. This handles the case where the executor is between checks.

**Rationale**: Belt-and-suspenders approach — the executor checks the kill switch directly for fast response, and the GUI polls as a backup to ensure UI state updates.

**Alternatives considered**:
- Relying solely on executor's direct check: Works for stopping execution, but the GUI won't know to update until `_on_complete` fires. Adding the GUI poll ensures immediate UI feedback.

### 4. pynput keyboard listener cross-platform reliability

**Finding**: From the coordinate picker work earlier in this session, pynput's `mouse.Listener` crashes on macOS, but `keyboard.Listener` works fine. The existing `KillSwitch` uses only `keyboard.Listener`, which is confirmed working on both macOS and Windows.

**Decision**: No changes needed to the kill switch listener itself. Keep using pynput keyboard-only listener.

**Rationale**: Already validated in the existing codebase and confirmed working in this session.
