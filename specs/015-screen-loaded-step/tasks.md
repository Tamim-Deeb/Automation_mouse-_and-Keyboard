# Tasks: Screen Loaded Step

**Input**: Design documents from `/specs/015-screen-loaded-step/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested — test tasks omitted.

**Organization**: Single user story — tasks organized sequentially with parallel opportunities noted.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the SCREEN_LOADED step type and validation

- [X] T001 Add SCREEN_LOADED enum value to StepType in src/workflow/models.py
- [X] T002 Add SCREEN_LOADED validation logic to WorkflowStep.validate() in src/workflow/models.py — requires start_x, start_y, end_x, end_y (integers) and max_tries (integer, minimum 1)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Wire up the step in the GUI and executor

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Add "Screen Loaded" button to AddStepDialog step type list in src/gui/step_editors.py
- [X] T004 Create _create_screen_loaded_fields() method in StepEditorDialog in src/gui/step_editors.py — start/end coordinate fields with Pick buttons (same pattern as Click And Move) plus a "Max Tries" entry field with default value 10
- [X] T005 Add SCREEN_LOADED case to StepEditorDialog._create_widgets() to call _create_screen_loaded_fields() in src/gui/step_editors.py
- [X] T006 Add SCREEN_LOADED save validation to StepEditorDialog._on_save() in src/gui/step_editors.py — collect start_x, start_y, end_x, end_y as integers and max_tries as integer (minimum 1)
- [X] T007 Add SCREEN_LOADED display format to WorkflowPanel._format_step() in src/gui/workflow_panel.py — show "Screen Loaded (start_x, start_y) → (end_x, end_y) [max: N]"
- [X] T008 Update WorkflowPanel._on_add_step() to pass on_pick_coords for SCREEN_LOADED step type (add to the list with CLICK, DOUBLE_CLICK, CLICK_AND_MOVE) in src/gui/workflow_panel.py
- [X] T009 Add SCREEN_LOADED case to WorkflowExecutor._format_step_detail() for logging in src/engine/executor.py

**Checkpoint**: Foundation ready — step type exists, GUI editor works with coordinate pickers

---

## Phase 3: User Story 1 - Wait for Screen Content to Load (Priority: P1) 🎯 MVP

**Goal**: Retry loop that clears clipboard, drags to select text, copies, checks clipboard — continues on success, stops workflow on max tries exceeded

**Independent Test**: Add a Screen Loaded step with coordinates over visible text, run workflow, verify it passes. Then point at blank area with max tries 2, verify workflow stops after 2 attempts.

### Implementation for User Story 1

- [X] T010 [US1] Register screen_loaded handler in MainApp._register_step_handlers() in src/main.py — implement retry loop: for each attempt up to max_tries: (1) clear clipboard, (2) wait 50ms, (3) mouse.drag(start_x, start_y, end_x, end_y), (4) wait 50ms, (5) pyautogui.hotkey('ctrl', 'c'), (6) wait 50ms, (7) check clipboard.paste().strip(), (8) if non-empty break success, (9) if empty and attempts remaining use interruptible_sleep(1000ms) with kill_switch, (10) if max tries exceeded call session.stop()

**Checkpoint**: Screen Loaded step fully functional — can add, configure, and execute with retry logic

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Serialization, dialog sizing, and validation

- [X] T011 Set dialog height for SCREEN_LOADED to 500 (5 coordinate fields + max tries + buttons) in StepEditorDialog.__init__() in src/gui/step_editors.py
- [X] T012 Verify WorkflowSerializer handles SCREEN_LOADED step save/load correctly (all 5 params) — the serializer is generic so this is a verification task
- [ ] T013 Run quickstart.md scenarios to validate end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (T001-T002)
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion
- **Polish (Phase 4)**: Depends on Phase 3 completion

### Within Each Phase

- T001 → T002 (validation depends on enum value)
- T003 → T004 → T005 → T006 (sequential GUI construction in same file)
- T007, T008 are in the same file (workflow_panel.py) — sequential
- T009 is independent (executor.py)
- T010 depends on all foundational tasks
- T011 depends on T004 (editor form exists)

### Parallel Opportunities

- T007+T009 can run in parallel (different files)
- T011 can run in parallel with T010 (different files)

---

## Implementation Strategy

### MVP First

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T009)
3. Complete Phase 3: User Story 1 (T010)
4. **STOP and VALIDATE**: Test Screen Loaded step with visible text and blank area
5. Complete Phase 4: Polish (T011-T013)

---

## Notes

- Handler retry loop is self-contained in main.py — no new module needed (per research.md Decision 1)
- Whitespace-only clipboard content is treated as empty (research.md Decision 2)
- Uses interruptible_sleep for retry waits to respect kill-switch (research.md Decision 3)
- On max tries exceeded, calls session.stop() — same mechanism as kill-switch (research.md Decision 4)
- Drag + copy timing: 50ms delays between operations (research.md Decision 5)
- Coordinate picker reuses Click And Move pattern (_on_start_coords_picked, _on_end_coords_picked)
- The handler needs access to kill_switch for interruptible sleep — pass via closure or check executor pattern
