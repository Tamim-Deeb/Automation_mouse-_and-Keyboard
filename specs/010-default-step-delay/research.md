# Research: Default Step Delay

## R1: Preferences Persistence Mechanism

**Decision**: Simple JSON file at `~/.automation-mouse/preferences.json`

**Rationale**: The project has no existing preferences system. A single JSON file in the user's home directory is the simplest approach that works cross-platform. The `WorkflowSerializer` already uses `json.dump`/`json.load` for workflow files, so the pattern is established in the codebase.

**Alternatives considered**:
- **Store in workflow file**: Rejected — the delay is a user preference, not a workflow property. Different users running the same workflow may want different delays.
- **Python `configparser` / INI file**: Rejected — adds complexity for a single integer value. JSON is already used elsewhere in the project.
- **Registry (Windows) / plist (macOS)**: Rejected — platform-specific, harder to debug, overkill for one setting.

**File format**:
```json
{
  "step_delay_ms": 200
}
```

## R2: Interruptible Delay Implementation

**Decision**: Reuse `WaitModule.interruptible_sleep(duration_ms, stop_event)` from `src/automation/wait.py`

**Rationale**: This method already exists (added in 009-safe-stop), uses `threading.Event.wait(timeout)` for non-blocking sleep, and integrates with the kill switch. No new delay mechanism needed.

**Alternatives considered**:
- **`time.sleep()` with periodic kill-switch checks**: Rejected — `interruptible_sleep` already solves this exact problem with sub-second responsiveness.
- **New delay function**: Rejected — would duplicate existing functionality.

## R3: Delay Placement in Execution Loop

**Decision**: Insert delay after each `_execute_step()` call in the step loop, before the next kill-switch check

**Rationale**: The executor's step loop in `execute()` already has a clear structure: check kill switch → execute step → (next iteration). Adding the delay after step execution and before the next iteration's kill-switch check ensures consistent timing. The delay applies after every step including WAIT steps, matching the spec requirement.

**Alternatives considered**:
- **Delay inside `_execute_step()`**: Rejected — mixes step logic with execution settings; harder to test independently.
- **Delay only between non-WAIT steps**: Rejected — spec explicitly says delay applies after WAIT steps too (acceptance scenario 3).

## R4: Input Validation Approach

**Decision**: Validate on focus-out and on Start button click; use tkinter's `validate` command with `%P` substitution for real-time numeric filtering

**Rationale**: tkinter's built-in entry validation (`validatecommand`) can restrict input to digits only. Final validation on Start ensures the value is within acceptable range (>= 0). This matches the existing pattern where `start_row` is validated on execution start.

**Alternatives considered**:
- **Spinbox widget**: Considered but rejected — ttk.Spinbox behavior varies across platforms and the existing UI uses Entry fields for consistency.
- **Post-hoc validation only**: Rejected — better UX to prevent non-numeric input in real-time.
