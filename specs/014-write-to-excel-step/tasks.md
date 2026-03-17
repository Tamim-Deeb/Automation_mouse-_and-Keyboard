# Tasks: Write To Excel Step

**Input**: Design documents from `/specs/014-write-to-excel-step/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested — test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the WRITE_TO_EXCEL step type and create the ExcelWriter module

- [X] T001 Add WRITE_TO_EXCEL enum value to StepType in src/workflow/models.py
- [X] T002 Add WRITE_TO_EXCEL validation logic to WorkflowStep.validate() in src/workflow/models.py (requires column_name: non-empty string, write_mode: "mark_done" or "paste_clipboard")
- [X] T003 Create ExcelWriter module in src/excel/writer.py with write_cell(file_path, sheet_name, row, column_name, value) method that opens workbook in write mode, finds column by header name, writes value, saves, and closes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Wire up the step in the GUI and executor so both user stories can use it

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add "Write To Excel" button to AddStepDialog step type list in src/gui/step_editors.py
- [X] T005 Create _create_write_to_excel_fields() method in StepEditorDialog in src/gui/step_editors.py — column dropdown (like INSERT_COLUMN_VALUE) + write mode radio/dropdown with "Mark Done (x)" and "Paste Clipboard" options
- [X] T006 Add WRITE_TO_EXCEL case to StepEditorDialog._create_widgets() to call _create_write_to_excel_fields() in src/gui/step_editors.py
- [X] T007 Add WRITE_TO_EXCEL save validation to StepEditorDialog._on_save() in src/gui/step_editors.py — collect column_name and write_mode params
- [X] T008 Add WRITE_TO_EXCEL display format to WorkflowPanel._format_step() in src/gui/workflow_panel.py — show "Write To Excel [column] (mode)"
- [X] T009 Add paste() method to ClipboardModule in src/automation/clipboard.py — returns pyperclip.paste() string
- [X] T010 Add WRITE_TO_EXCEL case to WorkflowExecutor._format_step_detail() for logging in src/engine/executor.py

**Checkpoint**: Foundation ready — step type exists, GUI editor works, ExcelWriter module available

---

## Phase 3: User Story 1 - Mark Done in Excel (Priority: P1) 🎯 MVP

**Goal**: Write "x" to a chosen column on the current row during workflow execution

**Independent Test**: Add a Write To Excel step with "Mark Done" mode, run workflow, verify "x" appears in the target column for each processed row

### Implementation for User Story 1

- [X] T011 [US1] Register write_to_excel handler in MainApp._register_step_handlers() in src/main.py — handler determines value based on write_mode, computes Excel row as session.current_row + 1, calls ExcelWriter.write_cell(); for "mark_done" mode, value is "x"
- [X] T012 [US1] Add set_columns() support to StepEditorDialog for WRITE_TO_EXCEL (reuse pattern from INSERT_COLUMN_VALUE) in src/gui/step_editors.py
- [X] T013 [US1] Update WorkflowPanel._on_add_step() to pass available_columns to WRITE_TO_EXCEL editor (same as INSERT_COLUMN_VALUE) in src/gui/workflow_panel.py

**Checkpoint**: Mark Done mode fully functional — can add step, configure column, execute, and verify "x" written to Excel

---

## Phase 4: User Story 2 - Paste Clipboard to Excel (Priority: P2)

**Goal**: Write clipboard content to a chosen column on the current row during workflow execution

**Independent Test**: Copy text to clipboard, run workflow with "Paste Clipboard" Write To Excel step, verify clipboard text appears in target column

### Implementation for User Story 2

- [X] T014 [US2] Update write_to_excel handler in src/main.py to handle "paste_clipboard" mode — call self.clipboard.paste() to get clipboard content, write to Excel cell

**Checkpoint**: Both Mark Done and Paste Clipboard modes work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Serialization, logging, and edge case handling

- [X] T015 Verify WorkflowSerializer handles WRITE_TO_EXCEL step save/load correctly (column_name and write_mode params) — test by saving and loading a workflow with a Write To Excel step
- [X] T016 Run quickstart.md scenarios (Mark Done, Paste Clipboard, Save/Load) to validate end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (T001-T003) — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion
- **User Story 2 (Phase 4)**: Depends on Phase 3 (T011 handler exists; T014 extends it)
- **Polish (Phase 5)**: Depends on Phase 3 and Phase 4 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on US1 handler registration (T011) — extends the handler with paste_clipboard mode

### Within Each Phase

- T001 → T002 (validation depends on enum value existing)
- T003 is independent of T001/T002
- T004 → T005 → T006 → T007 (sequential GUI construction)
- T008, T009, T010 are independent of each other
- T011 depends on T003 (ExcelWriter) and T009 (ClipboardModule.paste)
- T012, T013 depend on T005 (editor form exists)

### Parallel Opportunities

- T001+T003 can run in parallel (different files)
- T008, T009, T010 can run in parallel (different files)
- T012, T013 can run in parallel with T011 (different files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T010)
3. Complete Phase 3: User Story 1 (T011-T013)
4. **STOP and VALIDATE**: Test Mark Done mode independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test Mark Done independently → MVP!
3. Add User Story 2 → Test Paste Clipboard independently
4. Polish → Verify serialization and end-to-end scenarios

---

## Notes

- ExcelWriter opens/writes/saves/closes on each call (stateless per research.md Decision 2)
- Excel row = session.current_row + 1 (header is row 1, data starts row 2)
- Clipboard access via existing pyperclip dependency (ClipboardModule)
- Column dropdown reuses the same pattern as INSERT_COLUMN_VALUE step
- No new dependencies required
