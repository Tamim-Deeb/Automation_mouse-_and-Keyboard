# Tasks: Excel-Driven Desktop Automation Workflow Builder

**Input**: Design documents from `/specs/001-excel-automation-builder/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Integration tests included per constitution requirement (Principle V: every module MUST have at least one integration test).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and dependency management

- [x] T001 Create project directory structure per plan.md: src/, src/gui/, src/engine/, src/automation/, src/excel/, src/workflow/, src/logging/, tests/, tests/integration/
- [x] T002 Create requirements.txt with dependencies: pyautogui, openpyxl, pynput, pytest
- [x] T003 [P] Create all __init__.py files for src/ and subpackages
- [x] T004 [P] Create tests/conftest.py with shared pytest fixtures (sample Excel file fixture, sample workflow fixture)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models, automation modules, and infrastructure that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement Workflow and WorkflowStep dataclasses in src/workflow/models.py per data-model.md (step types enum, type-specific params dict, validation methods)
- [x] T006 [P] Implement step type registry in src/engine/step_registry.py (register/lookup step handlers by type string, extensible without modifying existing code per Constitution III)
- [x] T007 [P] Implement Excel reader module in src/excel/reader.py (load workbook, list sheets, select sheet, extract headers from row 1, iterate data rows with formatted cell values using number_format, read_only mode for large files, max 10,000 rows)
- [x] T008 [P] Implement mouse automation module in src/automation/mouse.py (single click at x,y and double click at x,y via pyautogui, screen bounds validation, configurable delay)
- [x] T009 [P] Implement keyboard automation module in src/automation/keyboard.py (type text character-by-character via pyautogui.write, press hotkey via pyautogui.hotkey for Enter/Backspace/Tab/Shift+Tab/Ctrl+A/Ctrl+C/Ctrl+V, configurable inter-key delay; Esc is reserved for kill-switch and excluded from hotkey list)
- [x] T010 [P] Implement wait module in src/automation/wait.py (sleep for specified duration_ms, minimum 50ms enforcement per constitution timing guard)
- [x] T011 [P] Implement action logger in src/logging/action_logger.py (write timestamped log entries to file, support DRY-RUN prefix, incremental file writes per data-model.md volume assumptions)
- [x] T012 Implement main application window shell in src/gui/app.py (tkinter root window with three-panel layout: excel panel top, workflow panel center, execution panel bottom; menu bar with File menu placeholder)

**Checkpoint**: Foundation ready — all core modules exist, user story implementation can begin

---

## Phase 3: User Story 1 — Build and Run a Basic Workflow (Priority: P1) MVP

**Goal**: User imports Excel, builds a step sequence, and executes it row-by-row with progress display and dry-run support

**Independent Test**: Create a 5-row Excel file with two columns, build a workflow with click + insert + hotkey steps, run it, and verify all 5 rows are processed with correct column values

### Integration Tests for User Story 1

- [x] T013 [P] [US1] Integration test for Excel reader in tests/integration/test_excel_reader.py (load sample .xlsx, verify headers, iterate rows, verify formatted values for dates/numbers/strings)
- [x] T014 [P] [US1] Integration test for executor in tests/integration/test_executor.py (build a workflow with multiple step types, run against sample Excel in dry-run mode, verify log contains correct actions for each row)
- [x] T038 [P] [US1] Integration test for mouse automation in tests/integration/test_mouse.py (verify click and double-click dispatch correctly, verify screen bounds check returns skip for invalid coords)
- [x] T039 [P] [US1] Integration test for keyboard automation in tests/integration/test_keyboard.py (verify character-by-character typing, verify each hotkey combo dispatches correctly — Enter, Backspace, Tab, Shift+Tab, Ctrl+A, Ctrl+C, Ctrl+V)
- [x] T040 [P] [US1] Integration test for wait module in tests/integration/test_wait.py (verify minimum 50ms enforcement, verify approximate timing accuracy)
- [x] T041 [P] [US1] Integration test for kill-switch in tests/integration/test_kill_switch.py (verify listener starts/stops, verify threading.Event is set on trigger, verify response time < 2 seconds)

### Implementation for User Story 1

- [x] T015 [P] [US1] Implement Excel panel GUI in src/gui/excel_panel.py (Import Excel button with file dialog, sheet dropdown populated from workbook, display column headers list, show row count)
- [x] T016 [P] [US1] Implement step editor forms in src/gui/step_editors.py (per-step-type parameter forms: x/y fields for click/double-click with Pick button, text field for type-text, duration field for wait, column dropdown for insert-column-value populated from Excel headers, hotkey dropdown for press-hotkey)
- [x] T017 [US1] Implement coordinate picker overlay in src/gui/coordinate_picker.py (transparent fullscreen tkinter overlay, capture mouse click x/y, return coordinates to calling form, Esc to cancel)
- [x] T018 [US1] Implement workflow panel GUI in src/gui/workflow_panel.py (step list display showing type and key params, Add Step button with step type selector, append new step to list)
- [x] T019 [US1] Implement execution engine in src/engine/executor.py (accept Workflow + ExcelDataSource + ExecutionSession, iterate rows from start_row, execute each step per row via step_registry, check kill-switch flag between steps, support dry_run flag to skip automation calls, log every action via action_logger, update current_row and status)
- [x] T020 [US1] Implement kill-switch listener in src/engine/kill_switch.py (pynput keyboard.Listener in daemon thread, listen for Esc key, set threading.Event on trigger, start/stop methods, register before execution per constitution)
- [x] T021 [US1] Implement execution panel GUI in src/gui/execution_panel.py (Start button, progress label showing "Row X of Y", start row number input field defaulting to 1, dry-run checkbox, run executor in background thread to keep GUI responsive)
- [x] T022 [US1] Wire all panels together in src/main.py (instantiate App with ExcelPanel, WorkflowPanel, ExecutionPanel; connect Excel import to step editors column dropdown; connect Start button to executor; connect kill-switch to executor stop flag)

**Checkpoint**: User Story 1 fully functional — user can import Excel, build steps, pick coordinates, and execute row-by-row with progress and dry-run

---

## Phase 4: User Story 2 — Save and Reload a Workflow (Priority: P2)

**Goal**: User saves a workflow to a JSON file and loads it back with 100% fidelity

**Independent Test**: Build a workflow with all 6 step types, save to JSON, reload, verify every step type and parameter matches

### Integration Tests for User Story 2

- [x] T023 [P] [US2] Integration test for workflow serializer in tests/integration/test_workflow_serializer.py (create workflow with all 6 step types, save to temp JSON file, load back, assert equality of every field per contracts/workflow-file-schema.json)

### Implementation for User Story 2

- [x] T024 [US2] Implement workflow serializer in src/workflow/serializer.py (save Workflow to JSON file matching contracts/workflow-file-schema.json schema, load Workflow from JSON file with validation, handle corrupted/invalid files with clear error messages, preserve step order and all params)
- [x] T025 [US2] Add Save/Load workflow to GUI in src/gui/app.py (File menu: Save Workflow with file dialog for .json, Load Workflow with file dialog, on load populate workflow panel with restored steps, error dialog on invalid file, do not lose in-memory workflow on load failure)

**Checkpoint**: User Stories 1 AND 2 functional — workflows persist across sessions

---

## Phase 5: User Story 3 — Stop Execution Safely (Priority: P2)

**Goal**: User can stop a running workflow at any time via Stop button or Esc hotkey; execution halts after current step with last-row-processed message

**Independent Test**: Start a workflow on a large dataset, trigger stop mid-execution, verify no actions occur after stop and last processed row is displayed

### Implementation for User Story 3

- [x] T026 [US3] Add Stop button to execution panel in src/gui/execution_panel.py (Stop button enabled only during execution, triggers kill-switch event, disable Start button during execution, re-enable after stop/completion)
- [x] T027 [US3] Implement stop status display in src/gui/execution_panel.py (after stop: show "Stopped at row X of Y" message, after completion: show "Completed all Y rows", update status label from executor callback)
- [x] T028 [US3] Connect Esc kill-switch to Stop button behavior in src/engine/executor.py (executor checks kill-switch event after each step, on trigger: set status to stopped, record last processed row, exit row loop cleanly)

**Checkpoint**: Safe execution control — user can always abort, system reports last processed row

---

## Phase 6: User Story 4 — Manage Workflow Steps (Priority: P3)

**Goal**: User can reorder, delete, and insert steps at any position in the workflow

**Independent Test**: Create a 5-step workflow, reorder step 3 to position 1, delete step 4, add new step at position 2, verify final order

### Implementation for User Story 4

- [x] T029 [US4] Add move-up and move-down buttons to workflow panel in src/gui/workflow_panel.py (select a step in the list, click Up/Down to swap positions, update step order indices in Workflow model)
- [x] T030 [P] [US4] Add delete step button to workflow panel in src/gui/workflow_panel.py (select a step, click Delete to remove it, re-index remaining steps, confirm if workflow has unsaved changes)
- [x] T031 [US4] Add insert-at-position capability to workflow panel in src/gui/workflow_panel.py (Add Step inserts after currently selected step instead of always appending, if no selection: append to end)

**Checkpoint**: All user stories independently functional — full workflow management

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling, validation hardening, and final quality checks

- [x] T032 [P] Add edge case handling for empty Excel cells in src/engine/executor.py (insert empty string for blank cells, continue execution)
- [x] T033 [P] Add edge case handling for zero-row worksheets in src/gui/execution_panel.py (show warning, disable Start button when no data rows)
- [x] T034 [P] Add edge case handling for out-of-bounds coordinates in src/automation/mouse.py (check screen size via pyautogui.size(), skip step and log warning if x/y exceed bounds)
- [x] T035 [P] Add edge case handling for duplicate column headers in src/excel/reader.py (use first occurrence, display warning to user)
- [x] T036 Validate application against quickstart.md scenarios in specs/001-excel-automation-builder/quickstart.md (manually run the "Your First Workflow" and "Example Workflow" scenarios end-to-end)
- [x] T037 Integration test for coordinate picker in tests/integration/test_coordinate_picker.py (verify overlay creates/destroys correctly, verify coordinate capture returns valid x,y tuple)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 — core MVP
- **User Story 2 (Phase 4)**: Depends on Phase 2 + needs Workflow model from Phase 2 — can run in parallel with US1 if desired
- **User Story 3 (Phase 5)**: Depends on Phase 3 (needs working executor and execution panel to add Stop)
- **User Story 4 (Phase 6)**: Depends on Phase 3 (needs working workflow panel to add reorder/delete)
- **Polish (Phase 7)**: Depends on Phases 3–6 being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependencies on other stories
- **US2 (P2)**: Can start after Phase 2 — independent of US1 (only needs Workflow model)
- **US3 (P2)**: Depends on US1 (needs executor and execution panel)
- **US4 (P3)**: Depends on US1 (needs workflow panel with step list)

### Within Each User Story

- Integration tests before implementation (write tests, verify they fail)
- GUI panels before wiring/integration
- Core logic before GUI integration
- Story complete before moving to next priority

### Parallel Opportunities

- Phase 1: T003 and T004 can run in parallel
- Phase 2: T006, T007, T008, T009, T010, T011 can all run in parallel (independent modules)
- Phase 3: T013+T014 (tests) in parallel; T015+T016 (GUI panels) in parallel
- Phase 4: T023 (test) can start immediately; T024 before T025
- Phase 6: T029+T030 in parallel (different UI elements)
- Phase 7: T032, T033, T034, T035 all in parallel

---

## Parallel Example: User Story 1

```bash
# Launch integration tests in parallel:
Task T013: "Integration test for Excel reader in tests/integration/test_excel_reader.py"
Task T014: "Integration test for executor in tests/integration/test_executor.py"

# Launch GUI panels in parallel:
Task T015: "Excel panel GUI in src/gui/excel_panel.py"
Task T016: "Step editor forms in src/gui/step_editors.py"
```

---

## Parallel Example: Phase 2 Foundational

```bash
# All independent modules can be built in parallel:
Task T006: "Step type registry in src/engine/step_registry.py"
Task T007: "Excel reader in src/excel/reader.py"
Task T008: "Mouse automation in src/automation/mouse.py"
Task T009: "Keyboard automation in src/automation/keyboard.py"
Task T010: "Wait module in src/automation/wait.py"
Task T011: "Action logger in src/logging/action_logger.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test US1 independently — import Excel, build workflow, execute, verify progress and dry-run
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo (save/load)
4. Add User Story 3 → Test independently → Demo (safe stop)
5. Add User Story 4 → Test independently → Demo (step management)
6. Polish → Final validation against quickstart.md

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution requires: kill-switch before execution, dry-run mode, timing guards (50ms min), timestamped logging
