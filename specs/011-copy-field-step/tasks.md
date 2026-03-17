# Tasks: Copy Field Step

**Input**: Design documents from `/specs/011-copy-field-step/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in the spec. Test tasks are omitted.

**Organization**: Single user story — tasks are ordered by dependency.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Add pyperclip dependency

- [x] T001 Add `pyperclip` to `requirements.txt` for clipboard operations

**Checkpoint**: Dependency available for import

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the new step type and clipboard module

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 [P] Add `COPY_FIELD = "copy_field"` to `StepType` enum in `src/workflow/models.py`
- [x] T003 [P] Create `src/automation/__init__.py` (if missing) and `src/automation/clipboard.py` — implement a `ClipboardModule` class with a `clear()` method that calls `pyperclip.copy('')` to empty the system clipboard

**Checkpoint**: COPY_FIELD step type exists and clipboard can be cleared programmatically

---

## Phase 3: User Story 1 - Copy Field Step Type (Priority: P1) 🎯 MVP

**Goal**: User can add a "Copy Field" step that clears clipboard, selects all, and copies

**Independent Test**: Add Copy Field step, focus a text field with known content, run workflow, verify clipboard contains the text

### Implementation for User Story 1

- [x] T004 [US1] Register `copy_field_handler` in `_register_step_handlers()` in `src/main.py` — the handler must: (1) call `ClipboardModule().clear()`, (2) sleep 50ms, (3) call `pyautogui.hotkey('ctrl', 'a')`, (4) sleep 50ms, (5) call `pyautogui.hotkey('ctrl', 'c')`; import `ClipboardModule` from `src.automation.clipboard` and `time` for delays
- [x] T005 [US1] Add "Copy Field" to the step type button list in `StepTypeChooser` in `src/gui/step_editors.py` — add `(StepType.COPY_FIELD, "Copy Field")` to the `step_types` list
- [x] T006 [US1] Handle Copy Field in `StepEditorDialog` in `src/gui/step_editors.py` — since Copy Field has no parameters, the editor should show no input fields (no `elif` branch needed for form creation); in `_on_save()`, add `elif self.step_type == StepType.COPY_FIELD:` with `self.params = {}`
- [x] T007 [US1] Add Copy Field display format in `_format_step()` in `src/gui/workflow_panel.py` — add `elif step.type == StepType.COPY_FIELD:` with `params = ""` (no parameters to display); the step type label "Copy Field" is auto-generated from the enum value

**Checkpoint**: Copy Field step can be added, displayed, executed, saved, and loaded

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation and edge cases

- [x] T008 Ensure Copy Field step passes validation in `WorkflowStep.validate()` in `src/workflow/models.py` — add no validation rules (empty params is valid); verify the step does not trigger any validation errors
- [x] T009 Run quickstart.md validation — manually test the full flow described in `specs/011-copy-field-step/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Can start in parallel with Phase 1
- **User Story 1 (Phase 3)**: Depends on Phase 1 (T001) and Phase 2 (T002, T003)
- **Polish (Phase 4)**: Depends on Phase 3

### Within User Story 1

- T004 depends on T002 (StepType enum) and T003 (ClipboardModule)
- T005 depends on T002 (StepType enum)
- T006 depends on T002 (StepType enum)
- T007 depends on T002 (StepType enum)
- T004, T005, T006, T007 can run in parallel (different files)

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T004, T005, T006, T007 can all run in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Launch both foundational tasks together:
Task: "Add COPY_FIELD to StepType enum in src/workflow/models.py"
Task: "Create ClipboardModule in src/automation/clipboard.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001) + Phase 2: Foundational (T002, T003) — in parallel
2. Complete Phase 3: User Story 1 (T004–T007) — in parallel
3. **STOP and VALIDATE**: Add Copy Field step, run on a text field, verify clipboard contains the text
4. Deploy if ready — feature is complete

### Incremental Delivery

1. T001 + T002 + T003 → Foundation ready
2. T004–T007 → Copy Field step works end-to-end (MVP!)
3. T008–T009 → Validation and testing

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- One new file: `src/automation/clipboard.py`; all other changes modify existing files
- The step auto-displays as "Copy Field" via the existing `_format_step()` logic: `step.type.value.replace('_', ' ').title()`
- Serialization works automatically — `WorkflowSerializer` handles the enum value string and empty params dict
- pyperclip must be added to `requirements-build.txt` as well if it needs to be bundled in the portable app
- Commit after each task or logical group
