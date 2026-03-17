# Tasks: Custom Hotkey Input

**Input**: Design documents from `/specs/012-custom-hotkey-input/`
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

**Purpose**: Add custom hotkey execution support to the keyboard automation layer

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 Add `press_custom_hotkey(hotkey_str: str)` method to `KeyboardAutomation` in `src/automation/keyboard.py` — the method must: (1) convert `hotkey_str` to lowercase, (2) split on `+` to get individual key names, (3) call `pyautogui.hotkey(*keys)`, (4) apply the inter-key delay; return True on success, False on failure with a warning
- [x] T002 Update `press_hotkey_by_string()` in `src/automation/keyboard.py` — modify the existing method to: first try `Hotkey(hotkey_str)` enum lookup (existing behavior), and if `ValueError` is raised, call `self.press_custom_hotkey(hotkey_str)` as fallback instead of just warning

**Checkpoint**: KeyboardAutomation can execute arbitrary key combinations via string input

---

## Phase 3: User Story 1 - Custom Hotkey via Freeform Input (Priority: P1) 🎯 MVP

**Goal**: User can type a custom hotkey combination in two input boxes (modifier + key) instead of being limited to the dropdown

**Independent Test**: Add a Press Hotkey step, type "ctrl" in modifier and "f1" in key, save, run workflow, verify Ctrl+F1 is pressed

### Implementation for User Story 1

- [x] T003 [P] [US1] Add custom hotkey input fields to `_create_hotkey_field()` in `src/gui/step_editors.py` — below the existing hotkey dropdown, add: (1) a label "— OR enter custom hotkey —", (2) a "Modifier (optional)" label and text entry (`self.modifier_entry`), (3) a "Key" label and text entry (`self.key_entry`)
- [x] T004 [US1] Update `_on_save()` in `src/gui/step_editors.py` — modify the `PRESS_HOTKEY` branch: if `self.key_entry.get().strip()` is non-empty, build the hotkey string as `modifier.lower() + "+" + key.lower()` (or just `key.lower()` if no modifier); if key is empty but modifier is filled, show validation error "Key is required for custom hotkey"; if both custom fields are empty, use the dropdown value (existing behavior)
- [x] T005 [US1] Update `press_hotkey_handler` in `src/main.py` — no code change needed since `press_hotkey_by_string()` already handles both enum values and custom strings after T002; verify the handler works with custom hotkey strings
- [x] T006 [US1] Verify workflow display in `_format_step()` in `src/gui/workflow_panel.py` — custom hotkey values display correctly since the existing format shows `step.params.get("hotkey", "")` which works for any string; no code change expected

**Checkpoint**: Custom hotkey steps can be added, displayed, executed, saved, and loaded

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation and end-to-end testing

- [x] T007 Ensure custom hotkey steps pass validation in `WorkflowStep.validate()` in `src/workflow/models.py` — the existing `PRESS_HOTKEY` validation checks if hotkey is in the `Hotkey` enum values; update to also accept any non-empty string (custom hotkeys) by removing or relaxing the enum-only check
- [x] T008 Run quickstart.md validation — manually test all 7 scenarios described in `specs/012-custom-hotkey-input/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **User Story 1 (Phase 3)**: Depends on Phase 2 (T001, T002)
- **Polish (Phase 4)**: Depends on Phase 3

### Within User Story 1

- T003 is independent (GUI only) — can start after Phase 2
- T004 depends on T003 (uses the entry widgets created in T003)
- T005 depends on T002 (relies on updated `press_hotkey_by_string`)
- T006 is verification only — can run anytime after T004

### Parallel Opportunities

- T001 and T002 are in the same file but T002 depends on T001 — must be sequential
- T003 can run in parallel with Phase 2 (different file)
- T005 and T006 are verification tasks — can run in parallel after T004

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (T001, T002) — keyboard layer supports custom hotkeys
2. Complete Phase 3: User Story 1 (T003, T004) — GUI input boxes added
3. **STOP and VALIDATE**: Add a custom hotkey step (e.g., Ctrl+F1), run workflow, verify it works
4. Deploy if ready — feature is complete

### Incremental Delivery

1. T001 + T002 → Keyboard layer ready
2. T003 + T004 → Custom hotkey GUI works end-to-end (MVP!)
3. T005 + T006 → Verification
4. T007 + T008 → Validation and testing

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- No new files created — all changes modify existing files (keyboard.py, step_editors.py, models.py)
- Custom hotkey strings stored in the same `params["hotkey"]` field as predefined hotkeys
- Serialization works automatically — `WorkflowSerializer` handles any string value in params
- The kill-switch suppress/unsuppress for Esc is already handled in executor.py; custom "escape" hotkey strings will also match since the handler checks `step.params.get("hotkey") == Hotkey.ESCAPE.value`
- Commit after each task or logical group
