# Data Model: Safe Stop (Esc Key Kill Switch)

**Feature Branch**: `009-safe-stop`
**Date**: 2026-03-16

## Entities

No new entities are introduced by this feature. The feature modifies the interactions between existing entities.

## Modified Interactions

### WorkflowExecutor ↔ KillSwitch (NEW connection)

Currently `WorkflowExecutor` has no reference to `KillSwitch`. After this feature:

- `WorkflowExecutor` receives a `KillSwitch` instance at construction time
- Between each step execution, the executor checks `kill_switch.is_triggered()`
- If triggered, the executor sets `session.status` to stopped and exits the loop

### WaitModule ↔ KillSwitch Event (NEW connection)

Currently `WaitModule.sleep()` uses blocking `time.sleep()`. After this feature:

- `WaitModule` gains an `interruptible_sleep(duration_ms, stop_event)` method
- When a `threading.Event` is provided, uses `event.wait(timeout)` instead of `time.sleep()`
- Returns immediately if the event is set (Esc pressed)
- Returns a boolean indicating whether the sleep was interrupted

### ExecutionPanel ↔ KillSwitch (ENHANCED connection)

Currently `ExecutionPanel` creates the `KillSwitch` but only uses it for the Stop button. After this feature:

- `ExecutionPanel` passes the `KillSwitch` to the `WorkflowExecutor`
- `ExecutionPanel` polls `kill_switch.is_triggered()` to update UI state

## State Transitions

### Execution Session Status

```
idle → running → completed    (normal flow, unchanged)
idle → running → stopped      (Stop button OR Esc key)
```

The `stopped` state is already supported. The only change is that Esc key now triggers it via the kill switch → executor path.
