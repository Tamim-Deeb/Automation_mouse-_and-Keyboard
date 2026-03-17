# Data Model: Default Step Delay

## Entities

### UserPreferences

Represents application-wide user settings that persist across sessions.

| Field | Type | Constraints | Default |
|-------|------|-------------|---------|
| step_delay_ms | integer | >= 0 | 200 |

**Storage**: JSON file at `~/.automation-mouse/preferences.json`

**Lifecycle**:
- Created on first write (when user changes delay from default)
- Read on application startup
- Updated whenever user changes the delay value and starts execution
- Directory created automatically if it doesn't exist

**Relationships**:
- Read by `ExecutionPanel` on initialization to populate the delay input field
- Passed to `WorkflowExecutor` as a parameter at execution start
- Independent of `Workflow` and `ExecutionSession` models — not part of workflow data

### ExecutionSession (existing, extended)

The existing `ExecutionSession` model does not need modification. The step delay is passed directly to the executor as a constructor parameter, keeping execution settings separate from the session model.

## State Transitions

UserPreferences has no state transitions — it is a simple key-value store with load/save operations.

## Validation Rules

- `step_delay_ms` must be a non-negative integer (>= 0)
- If preferences file is missing or corrupted, fall back to default value (200ms)
- If preferences file contains unknown keys, ignore them (forward compatibility)
