# Tasks: UI Polish & Visual Enhancement

**Input**: Design documents from `/specs/017-ui-polish/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Create the theme module that all user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 Create src/gui/theme.py with centralized color palette constants (dark header: #2b2b2b, light panel: #f5f5f5, button blue: #4a90d9, hover blue: #357abd, pressed blue: #2a5f9e, text dark: #333333, text light: #ffffff, border gray: #cccccc, highlight green: #90EE90), a function to initialize ttk.Style with "clam" theme, and custom style definitions for Dark.TFrame, Light.TFrame, Custom.TButton (with hover/pressed map), styled TLabelframe, and a center_dialog(dialog) helper function that calls update_idletasks() then positions the dialog at screen center with screen-bounds clamping: clamp x to max(0, min(x, screen_width - dialog_width)) and y to max(0, min(y, screen_height - dialog_height)) so dialogs never open partially off-screen (FR-004).
- [x] T002 Apply theme initialization in src/main.py: import and call the theme setup function from theme.py BEFORE creating the UI (before self._create_ui()), ensuring "clam" theme is active before any widgets are created.

**Checkpoint**: Theme module exists with all colors, styles, and centering utility. App uses "clam" theme.

---

## Phase 2: User Story 1 + User Story 2 — Dialog Sizing & Centering (Priority: P1) MVP

**Goal**: All dialogs open at proper sizes showing all content, and all dialogs open centered on screen.

**Independent Test (US1)**: Click "Add Step" — all 11 step type buttons are visible without scrolling, and the dialog is centered on screen.

**Independent Test (US2)**: Open any dialog (Add Step, Step Editor, confirmation, About) — each one appears centered on the screen.

### Implementation

- [x] T003 [US1] Update AddStepDialog in src/gui/step_editors.py: change geometry from "300x450" to "320x580" so all 11 step type buttons plus Cancel are visible without scrolling. Import center_dialog from theme.py and call it after geometry is set and widgets are created.
- [x] T004 [US2] Update StepEditorDialog in src/gui/step_editors.py: import center_dialog from theme.py and call it after dialog geometry is set and widgets are created. Verify each step type's dialog_height is sufficient for its content (Click: 300, Double Click: 300, Type Text: 300, Wait: 300, Insert Column Value: 300, Press Hotkey: 350, Click And Move: 450, Write To Excel: 350, Screen Loaded: 500, Condition: 350). Also ensure the dialog re-centers when it becomes visible again after a coordinate-pick action returns (FR-005) — call center_dialog() in the pick callback after the dialog is deiconified/raised.
- [x] T005 [P] [US2] Update confirmation/message dialogs in src/gui/workflow_panel.py: tkinter messagebox dialogs (showwarning, askyesno) are system dialogs and already center — no changes needed. Verify this is the case by testing. If any custom Toplevel dialogs exist, add centering.
- [x] T006 [P] [US2] Update About dialog in src/gui/app.py: if the About dialog uses messagebox.showinfo, it already centers (system dialog). Verify no custom Toplevel is used. Apply theme styles to the main window title bar area.

**Checkpoint**: Add Step dialog shows all 11 buttons without scrolling. All dialogs open centered on screen.

---

## Phase 3: User Story 3 — Professional Color Theme & Visual Styling (Priority: P2)

**Goal**: Application displays a cohesive two-tone color scheme with dark header, light panels, styled buttons with hover effects, and themed listbox.

**Independent Test**: Launch the application — dark header/toolbar area visible, light content panels, buttons change color on hover, step list has proper styling.

### Implementation

- [x] T007 [US3] Style the main window and menu bar in src/gui/app.py: set root window background to dark (#2b2b2b), apply Dark.TFrame style to the top-level container, apply Light.TFrame or default background to the three panel LabelFrames (Excel, Workflow, Execution), style the menu bar with dark background and light text if possible (tk.Menu configure).
- [x] T008 [US3] Style all buttons across the application to use Custom.TButton style (defined in theme.py) with blue background, white text, and hover/pressed color changes. Apply in src/gui/app.py, src/gui/workflow_panel.py (Add Step, Move Up, Move Down, Delete Step, Clear All), src/gui/execution_panel.py (Start, Stop), src/gui/excel_panel.py (Import Excel), and src/gui/step_editors.py (Save, Cancel, Pick buttons in all editors, step type buttons in AddStepDialog).
- [x] T009 [US3] Style the workflow step Listbox in src/gui/workflow_panel.py: set font to a readable size (e.g., ('TkDefaultFont', 10)), set default background to white (#ffffff), foreground to dark (#333333), selectbackground to button blue (#4a90d9), selectforeground to white. Ensure condition coloring (#CCE5FF, #FFFFCC) is still applied via _apply_condition_coloring() after the base styling.
- [x] T010 [P] [US3] Style the Excel panel in src/gui/excel_panel.py: apply themed styles to the Import button (Custom.TButton), file label, sheet dropdown, headers listbox (readable font, proper colors), and row count label. Ensure the panel background matches the light content theme.
- [x] T011 [P] [US3] Style the Execution panel in src/gui/execution_panel.py: apply themed styles to Start/Stop buttons (Custom.TButton), labels (Start Row, Delay, Dry Run), and entry fields. Ensure the panel background matches the light content theme.

**Checkpoint**: Application displays cohesive two-tone theme. Buttons have hover effects. All panels are visually distinct and professionally styled.

---

## Phase 4: User Story 4 — Step Addition Highlight Animation (Priority: P3)

**Goal**: Newly added steps flash with a green highlight for ~500ms before settling to their correct color.

**Independent Test**: Add a new step — it briefly flashes green then settles to white (or blue/yellow if under a Condition).

### Implementation

- [x] T012 [US4] Add highlight_new_step() method to WorkflowPanel in src/gui/workflow_panel.py: after inserting a new step in _on_add_step() and calling _update_display(), set the new step's listbox row background to highlight green (#90EE90), then schedule an after(500) callback that calls _apply_condition_coloring() to reset all rows to their correct colors (white, or blue/yellow for condition-governed steps). This ensures the highlight always settles to the correct final color.

**Checkpoint**: New steps flash green for 500ms then settle to correct color. Condition coloring preserved.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling, regression verification, visual consistency check

- [x] T013 Verify all existing tests pass without modification by running pytest from the repository root. No test code should need changes — this is a visual-only feature. Fix any regressions caused by theme changes (e.g., if tests import from gui modules that now require theme initialization).
- [x] T014 Verify edge cases: test on small screen resolution (resize window to 1024x768 — dialogs should clamp within bounds), test with 30+ steps in the workflow list (performance and coloring should not degrade), verify condition step coloring (blue #CCE5FF and yellow #FFFFCC) still displays correctly over the new theme. Test Add Step dialog with all 11 step types visible.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: No dependencies — start immediately
- **US1+US2 (Phase 2)**: Depends on Phase 1 (needs theme module and center_dialog helper)
- **US3 (Phase 3)**: Depends on Phase 1 (needs theme styles). Can run in parallel with Phase 2 (different concerns: sizing/centering vs colors)
- **US4 (Phase 4)**: Depends on Phase 3 (needs themed listbox styling to determine correct settle colors). Can overlap with late Phase 2 work.
- **Polish (Phase 5)**: Depends on all previous phases

### Within Phase 2

- T003 and T004 are sequential (same file: step_editors.py)
- T005 and T006 are parallelizable [P] (different files: workflow_panel.py and app.py)
- T005 and T006 can run in parallel with T003/T004

### Within Phase 3

- T007 must be first (sets main window theme that other panels inherit)
- T008 depends on T007 (button styles applied after main theme)
- T009 depends on T007 (listbox styling after main theme)
- T010 and T011 are parallelizable [P] (different files: excel_panel.py and execution_panel.py)

### Parallel Opportunities

- T005 + T006: Different files, no dependencies — run in parallel
- T010 + T011: Different files, no dependencies — run in parallel
- Phase 2 (sizing/centering) + Phase 3 (colors): Mostly independent — can overlap

---

## Parallel Example: Phase 2

```bash
# Sequential (same file):
Task T003: "Update AddStepDialog sizing in src/gui/step_editors.py"
Task T004: "Center StepEditorDialog in src/gui/step_editors.py"

# In parallel with above (different files):
Task T005: "Verify workflow_panel.py dialogs in src/gui/workflow_panel.py"
Task T006: "Verify About dialog in src/gui/app.py"
```

---

## Implementation Strategy

### MVP First (Phase 1 + Phase 2)

1. Complete Phase 1: Create theme module with colors and centering utility
2. Complete Phase 2: Fix dialog sizing and centering
3. **STOP and VALIDATE**: All dialogs open properly sized and centered
4. The biggest pain point (small Add Step dialog) is resolved

### Incremental Delivery

1. Phase 1 → Theme foundation ready
2. Phase 2 → Dialogs sized and centered (MVP!)
3. Phase 3 → Professional color theme applied
4. Phase 4 → Step highlight animation adds final polish
5. Phase 5 → Edge cases verified, tests pass
6. Each phase adds visual value without breaking previous phases

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1 and US2 share Phase 2 because both involve dialog changes in the same files
- No new integration tests required per constitution V (no new automation module)
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
