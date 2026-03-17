# Tasks: Default Step Delay

**Input**: Design documents from `/specs/010-default-step-delay/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in the spec. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Create the new preferences module

- [X] T001 Create `src/preferences/__init__.py` and `src/preferences/preferences.py` — implement `load_preferences()` and `save_preferences()` functions that read/write `~/.automation-mouse/preferences.json`; create directory if missing; return default `{"step_delay_ms": 200}` if file missing or corrupted; ignore unknown keys for forward compatibility

**Checkpoint**: Preferences module ready — can load/save step_delay_ms values

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add step_delay_ms parameter to the executor

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Add optional `step_delay_ms` parameter (default `0`) to `WorkflowExecutor.__init__()` in `src/engine/executor.py` — store as `self.step_delay_ms`

**Checkpoint**: Foundation ready — executor accepts step delay parameter

---

## Phase 3: User Story 1 - Configurable Default Delay Between Steps (Priority: P1) 🎯 MVP

**Goal**: User sets a delay value in the execution panel; during execution, that delay is inserted after each step

**Independent Test**: Create a workflow with 3+ steps, set delay to 1000ms, run and observe ~1s pause between each step

### Implementation for User Story 1

- [X] T003 [US1] Add interruptible delay after each step in `WorkflowExecutor.execute()` step loop in `src/engine/executor.py` — after `_execute_step()` returns and before the next kill-switch check, if `self.step_delay_ms > 0`, call `WaitModule.interruptible_sleep(self.step_delay_ms, self.kill_switch.event)` (or `WaitModule.sleep(self.step_delay_ms)` if no kill switch); if interrupted, call `self.session.stop()`
- [X] T004 [US1] Add "Delay (ms)" input field to `ExecutionPanel` in `src/gui/execution_panel.py` — add a labeled Entry field (width=8, default "200") next to the Dry Run checkbox; use tkinter `validatecommand` with `%P` substitution to accept only non-negative integers
- [X] T005 [US1] Pass `step_delay_ms` from `ExecutionPanel` to `WorkflowExecutor` constructor in `src/gui/execution_panel.py` — in `_on_start()`, read the delay entry value, validate it (>= 0, default to 200 if empty), and pass `step_delay_ms=value` to `WorkflowExecutor(...)`
- [X] T006 [US1] Ensure delay applies in dry-run mode in `src/engine/executor.py` — verify the delay is inserted after each step regardless of whether `session.dry_run` is True or False (the delay code path should not be inside any dry-run conditional)

**Checkpoint**: At this point, the user can set a delay between steps and it works during execution including kill-switch interruption

---

## Phase 4: User Story 2 - Delay Value Persistence Across Sessions (Priority: P2)

**Goal**: The last-used delay value is saved and restored when the application reopens

**Independent Test**: Set delay to 750ms, close and reopen the app, verify the delay field shows 750ms

### Implementation for User Story 2

- [X] T007 [US2] Load saved delay on startup in `ExecutionPanel.__init__()` in `src/gui/execution_panel.py` — call `load_preferences()` and set the delay entry field value to the stored `step_delay_ms` (or 200 if not found)
- [X] T008 [US2] Save delay on execution start in `ExecutionPanel._on_start()` in `src/gui/execution_panel.py` — after validating the delay value, call `save_preferences({"step_delay_ms": value})` to persist the current setting

**Checkpoint**: Delay value persists across application restarts

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and validation

- [X] T009 Handle edge cases in delay input validation in `src/gui/execution_panel.py` — ensure empty field defaults to 200ms on Start; negative values are rejected; field shows "ms" label for clarity
- [X] T010 Run quickstart.md validation — manually test the full flow described in `specs/010-default-step-delay/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Can start in parallel with Phase 1 (different files)
- **User Story 1 (Phase 3)**: Depends on Phase 1 (T001) and Phase 2 (T002)
- **User Story 2 (Phase 4)**: Depends on Phase 1 (T001) and Phase 3 (T004 — delay field must exist)
- **Polish (Phase 5)**: Depends on Phase 3 and Phase 4

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup + Foundational — no dependencies on other stories
- **User Story 2 (P2)**: Depends on US1's delay field (T004) being in place

### Within Each User Story

- T003 modifies executor step loop — must come before T006 (dry-run verification)
- T004 creates the UI field — must come before T005 (wiring to executor)
- T007 and T008 can run in parallel (different methods in same file, but T007 is init, T008 is on_start)

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T003 and T004 can run in parallel (different files)
- T007 and T008 can run in parallel (different methods)

---

## Parallel Example: Setup + Foundational

```bash
# Launch both foundational tasks together:
Task: "Create preferences module in src/preferences/preferences.py"
Task: "Add step_delay_ms parameter to WorkflowExecutor in src/engine/executor.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001) + Phase 2: Foundational (T002) — in parallel
2. Complete Phase 3: User Story 1 (T003–T006)
3. **STOP and VALIDATE**: Set delay to 1000ms, run a workflow, verify ~1s pauses between steps; press Esc during a delay to verify interruption
4. Deploy if ready — core delay feature is complete

### Incremental Delivery

1. T001 + T002 → Foundation ready
2. T003–T006 → Delay between steps works (MVP!)
3. T007–T008 → Delay value remembered across sessions
4. T009–T010 → Edge cases and validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All changes modify existing files except T001 (new preferences module)
- Reuses existing `WaitModule.interruptible_sleep()` from 009-safe-stop — no new delay mechanism needed
- Backward compatibility maintained — `step_delay_ms=0` keeps old behavior
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
