# Tasks: Safe Stop (Esc Key Kill Switch)

**Input**: Design documents from `/specs/009-safe-stop/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in the spec. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: No new project setup needed — all changes modify existing files. This phase is empty.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core changes that both user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Add `interruptible_sleep(duration_ms, stop_event)` method to `WaitModule` in `src/automation/wait.py` — uses `threading.Event.wait(timeout)` instead of `time.sleep()`, returns `True` if interrupted, enforces 50ms minimum delay
- [x] T002 [P] Add optional `kill_switch` parameter to `WorkflowExecutor.__init__()` in `src/engine/executor.py` — store as `self.kill_switch`, default `None` for backward compatibility

**Checkpoint**: Foundation ready — executor accepts kill switch, wait module supports interruptible sleep

---

## Phase 3: User Story 1 - Emergency Stop During Execution (Priority: P1) 🎯 MVP

**Goal**: Pressing Esc immediately stops workflow execution, including interrupting long waits

**Independent Test**: Start a multi-row workflow, press Esc during execution, verify it stops within 1 second and reports the correct stopped row

### Implementation for User Story 1

- [x] T003 [US1] Add kill-switch check in `WorkflowExecutor.execute()` row loop in `src/engine/executor.py` — after processing each row, check `self.kill_switch.is_triggered()` and call `self.session.stop()` if true
- [x] T004 [US1] Add kill-switch check in `WorkflowExecutor.execute()` step loop in `src/engine/executor.py` — before each `_execute_step()` call, check `self.kill_switch.is_triggered()` and break if true
- [x] T005 [US1] Update wait step handling in `WorkflowExecutor._execute_step()` in `src/engine/executor.py` — when step type is WAIT and kill_switch is provided, use `WaitModule.interruptible_sleep(duration, kill_switch.event)` instead of `WaitModule.sleep()`; if interrupted (returns True), call `self.session.stop()`
- [x] T006 [US1] Pass `kill_switch` from `ExecutionPanel` to `WorkflowExecutor` constructor in `src/gui/execution_panel.py` — update the `WorkflowExecutor(...)` call in `_on_start()` to include `kill_switch=self.kill_switch`
- [x] T007 [US1] Add kill-switch polling in `ExecutionPanel` in `src/gui/execution_panel.py` — add `_poll_kill_switch()` method that checks `kill_switch.is_triggered()` every 200ms using `self.parent.after()`, and calls `self.executor.stop()` when triggered; start polling in `_on_start()`, stop in `_update_complete()`

**Checkpoint**: At this point, pressing Esc during execution stops the workflow within 1 second, including during long waits

---

## Phase 4: User Story 2 - Visual Feedback on Safe Stop (Priority: P2)

**Goal**: User receives clear visual confirmation that the workflow was stopped by Esc, including which row it stopped on

**Independent Test**: Trigger Esc during execution, verify status label shows stopped row, completion dialog indicates user-initiated stop

### Implementation for User Story 2

- [x] T008 [US2] Update `_update_complete()` in `src/gui/execution_panel.py` — differentiate between Esc-triggered stop and normal stop button; when kill switch is triggered, show "Stopped by Esc at row X of Y" in the completion dialog instead of generic stop message
- [x] T009 [US2] Ensure `_poll_kill_switch()` in `src/gui/execution_panel.py` updates the progress label immediately when Esc is detected — set `progress_label` text to "Stopping..." before waiting for executor to finish

**Checkpoint**: User sees clear feedback distinguishing Esc stop from button stop, with correct row information

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases and cleanup

- [x] T010 Ensure kill switch listener is cleanly released on all exit paths (FR-006) in `src/gui/execution_panel.py` — verify `kill_switch.start()` is called only in `_on_start()` and `kill_switch.stop()` is called in `_update_complete()`, `reset()`, and after errors; confirm Esc has no effect when idle (FR-007)
- [x] T011 Handle rapid multiple Esc presses in `src/engine/executor.py` — verify that `is_triggered()` check is idempotent and multiple triggers don't cause double-stop or errors
- [x] T012 Run quickstart.md validation — manually test the full flow described in `specs/009-safe-stop/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **User Story 1 (Phase 3)**: Depends on Phase 2 (T001, T002)
- **User Story 2 (Phase 4)**: Depends on Phase 3 (builds on T007's polling)
- **Polish (Phase 5)**: Depends on Phase 3 and Phase 4

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1's polling mechanism (T007) being in place

### Within Each User Story

- T003 and T004 modify the same method — must be sequential
- T005 depends on T001 (interruptible sleep) and T003/T004 (kill switch in executor)
- T006 depends on T002 (executor accepts kill switch)
- T007 depends on T006 (executor has kill switch wired)

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T008 and T009 can run in parallel within US2 (different concerns in same file, but T009 is additive)

---

## Parallel Example: Foundational Phase

```bash
# Launch both foundational tasks together:
Task: "Add interruptible_sleep() to WaitModule in src/automation/wait.py"
Task: "Add kill_switch parameter to WorkflowExecutor in src/engine/executor.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001, T002)
2. Complete Phase 3: User Story 1 (T003–T007)
3. **STOP and VALIDATE**: Press Esc during a running workflow — should stop within 1 second
4. Deploy if ready — core safety feature is complete

### Incremental Delivery

1. T001 + T002 → Foundation ready
2. T003–T007 → Esc stops execution (MVP!)
3. T008–T009 → Better visual feedback on Esc stop
4. T010–T012 → Edge cases and validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All changes modify existing files — no new files created
- The existing `KillSwitch` class needs no modifications
- Backward compatibility is maintained — `kill_switch=None` keeps old behavior
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
