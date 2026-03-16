# Quickstart: Safe Stop (Esc Key Kill Switch)

**Feature Branch**: `009-safe-stop`
**Date**: 2026-03-16

## What This Feature Does

Pressing the Esc key immediately stops a running workflow. The kill switch works globally (even when the app is minimized or unfocused) and interrupts long wait steps.

## How to Test

1. Open the app and create a workflow with several steps
2. Import an Excel file with multiple rows
3. Click Start to begin execution
4. Press Esc at any point during execution
5. Verify:
   - Execution stops within 1 second
   - Status shows which row was stopped on
   - Start button is re-enabled
   - You can start a new execution without restarting

## Key Changes (3 files)

### 1. `src/engine/executor.py`
- `WorkflowExecutor.__init__()` accepts an optional `kill_switch` parameter
- Between each step, checks `kill_switch.is_triggered()` and stops if true
- Wait steps use interruptible sleep when kill switch is provided

### 2. `src/automation/wait.py`
- New method: `interruptible_sleep(duration_ms, stop_event)` that wakes on event

### 3. `src/gui/execution_panel.py`
- Passes `kill_switch` to `WorkflowExecutor` constructor
- Polls kill switch state to update UI when Esc triggers a stop
