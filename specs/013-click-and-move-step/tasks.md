# Tasks: Click And Move Step

**Input**: Design documents from `/specs/013-click-and-move-step/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in the spec. Test tasks are omitted.

**Organization**: Single user story — tasks are ordered by dependency.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: No setup needed — no new dependencies or files required.

(No tasks in this phase)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the new step type and drag method to the automation layer

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Add `CLICK_AND_MOVE = "click_and_move"` to `StepType` enum in `src/workflow/models.py`
- [x] T002 [P] Add `drag(start_x, start_y, end_x, end_y)` method to `MouseAutomation` in `src/automation/mouse.py` — the method must: (1) validate both coordinate pairs, (2) call `pyautogui.mouseDown(start_x, start_y)`, (3) call `pyautogui.moveTo(end_x, end_y, duration=0.5)`, (4) call `pyautogui.mouseUp()`, (5) apply delay; return True on success, False on failure with a warning

**Checkpoint**: CLICK_AND_MOVE step type exists and mouse can perform drag operations programmatically

---

## Phase 3: User Story 1 - Click And Move (Drag) Step (Priority: P1) 🎯 MVP

**Goal**: User can add a "Click And Move" step with start and end coordinates (each with a Pick button) that performs a mouse drag

**Independent Test**: Add a Click And Move step, pick start coords on a desktop icon, pick end coords on a folder, run workflow, verify the icon is dragged

### Implementation for User Story 1

- [x] T003 [US1] Add drag coordinate fields to `StepEditorDialog` in `src/gui/step_editors.py` — in `_create_widgets()`, add `elif self.step_type == StepType.CLICK_AND_MOVE:` that calls a new `_create_drag_coordinate_fields(container)` method; this method must create: (1) "Start Position" label, (2) Start X entry + Start Y entry + "Pick" button calling `self.on_pick_coords(self._on_start_coords_picked)`, (3) "End Position" label, (4) End X entry + End Y entry + "Pick" button calling `self.on_pick_coords(self._on_end_coords_picked)`; add `_on_start_coords_picked(x, y)` to populate `self.start_x_entry` and `self.start_y_entry`; add `_on_end_coords_picked(x, y)` to populate `self.end_x_entry` and `self.end_y_entry`
- [x] T004 [US1] Add save logic for Click And Move in `_on_save()` in `src/gui/step_editors.py` — add `elif self.step_type == StepType.CLICK_AND_MOVE:` that reads all four entries (`start_x_entry`, `start_y_entry`, `end_x_entry`, `end_y_entry`), validates they are integers (show validation error if not), and sets `self.params = {"start_x": ..., "start_y": ..., "end_x": ..., "end_y": ...}`
- [x] T005 [P] [US1] Add "Click And Move" to the step type button list in `AddStepDialog` in `src/gui/step_editors.py` — add `(StepType.CLICK_AND_MOVE, "Click And Move")` to the `step_types` list
- [x] T006 [US1] Enable coordinate picker for Click And Move in `src/gui/workflow_panel.py` — update the condition `if step_type in [StepType.CLICK, StepType.DOUBLE_CLICK]` to also include `StepType.CLICK_AND_MOVE` so that `on_pick_coords` is passed to the step editor
- [x] T007 [US1] Add Click And Move display format in `_format_step()` in `src/gui/workflow_panel.py` — add `elif step.type == StepType.CLICK_AND_MOVE:` with `params = f"({step.params.get('start_x', '')}, {step.params.get('start_y', '')}) → ({step.params.get('end_x', '')}, {step.params.get('end_y', '')})"`
- [x] T008 [US1] Register `click_and_move_handler` in `_register_step_handlers()` in `src/main.py` — the handler must call `self.mouse.drag(step.params["start_x"], step.params["start_y"], step.params["end_x"], step.params["end_y"])`; register with `register_step_handler(StepType.CLICK_AND_MOVE, click_and_move_handler)`

**Checkpoint**: Click And Move step can be added (with Pick buttons), displayed, executed, saved, and loaded

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation and end-to-end testing

- [x] T009 Add validation for Click And Move in `WorkflowStep.validate()` in `src/workflow/models.py` — add `elif self.type == StepType.CLICK_AND_MOVE:` that checks all four params (`start_x`, `start_y`, `end_x`, `end_y`) exist and are integers
- [x] T010 Run quickstart.md validation — manually test all 7 scenarios described in `specs/013-click-and-move-step/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **User Story 1 (Phase 3)**: Depends on Phase 2 (T001, T002)
- **Polish (Phase 4)**: Depends on Phase 3

### Within User Story 1

- T003 depends on T001 (StepType enum)
- T004 depends on T003 (uses the entry widgets created in T003)
- T005 depends on T001 (StepType enum)
- T006 depends on T001 (StepType enum)
- T007 depends on T001 (StepType enum)
- T008 depends on T001 (StepType enum) and T002 (drag method)

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T005 can run in parallel with T003 (different section of same file, but independent)
- T006 and T007 are in the same file but different methods — can be done together

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001, T002) — enum + drag method ready
2. Complete Phase 3: User Story 1 (T003–T008) — full GUI + execution
3. **STOP and VALIDATE**: Add a Click And Move step with Pick buttons, run workflow, verify drag works
4. Deploy if ready — feature is complete

### Incremental Delivery

1. T001 + T002 → Foundation ready
2. T003 + T004 + T005 → Step editor works
3. T006 + T007 + T008 → Picker, display, execution (MVP!)
4. T009 + T010 → Validation and testing

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- No new files created — all changes modify existing files (mouse.py, step_editors.py, workflow_panel.py, models.py, main.py)
- The coordinate picker callback pattern is reused from Click step — two separate callbacks target start vs end entry fields
- pyautogui drag uses mouseDown → moveTo(duration=0.5) → mouseUp for reliable drag detection
- Serialization works automatically — WorkflowSerializer handles the enum value string and params dict
- The step auto-displays as "Click And Move" via `step.type.value.replace('_', ' ').title()`
- Commit after each task or logical group
