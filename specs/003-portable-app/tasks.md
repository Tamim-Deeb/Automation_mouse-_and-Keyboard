# Tasks: Portable App Distribution

**Input**: Design documents from `/specs/003-portable-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested — test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and build tooling prerequisites

- [x] T001 Create application icon file at assets/app.ico (simple automation-themed icon, multi-size .ico with 16x16, 32x32, 48x48, 256x256)
- [x] T002 Update .gitignore to exclude dist/ and build/ directories
- [x] T003 Clean up requirements.txt — remove pyinstaller and pyinstaller-hooks-contrib from runtime deps, keep them as build-only deps in a separate requirements-build.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core build infrastructure that MUST be complete before any user story packaging can work

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create PyInstaller spec file at AutomationMouseKeyboard.spec with: entry point src/main.py, one-folder mode, windowed (no console), icon from assets/app.ico, hidden imports for pyautogui, pynput, openpyxl submodules
- [x] T005 Create build script at build.py that invokes PyInstaller using the .spec file, validates output exists in dist/AutomationMouseKeyboard/, and prints success/failure summary

**Checkpoint**: Build tooling ready — can now produce a packaged app folder

---

## Phase 3: User Story 1 - Launch App Without Installation (Priority: P1) MVP

**Goal**: Package the app so a non-technical user can double-click the .exe and see the full GUI with all features working — no Python install needed.

**Independent Test**: Copy dist/AutomationMouseKeyboard/ to a clean Windows machine (no Python), double-click AutomationMouseKeyboard.exe, verify main window appears within 10 seconds with all panels visible.

### Implementation for User Story 1

- [x] T006 [US1] Add frozen-app detection and startup error handling in src/main.py — wrap the main() function to catch exceptions and show a tkinter messagebox with user-friendly error instead of crashing silently (since console is hidden in packaged mode)
- [x] T007 [US1] Add resource path helper function in src/main.py — detect if running as frozen PyInstaller bundle (sys._MEIPASS) and resolve asset paths relative to the bundle directory
- [ ] T008 [US1] Run build.py and verify the output folder dist/AutomationMouseKeyboard/ contains AutomationMouseKeyboard.exe and _internal/ directory with all dependencies
- [ ] T009 [US1] Test launch: run dist/AutomationMouseKeyboard/AutomationMouseKeyboard.exe and verify the main GUI window appears with all panels (Excel, Workflow, Execution) and no console window is shown

**Checkpoint**: App launches from packaged .exe with full GUI — MVP complete

---

## Phase 4: User Story 2 - Download and Run from a Single Folder (Priority: P2)

**Goal**: Ensure the packaged folder is fully self-contained and portable — works from any location on disk without errors.

**Independent Test**: Copy the dist/AutomationMouseKeyboard/ folder to Desktop, Documents, and a USB drive path. Launch from each location and verify the app starts correctly.

### Implementation for User Story 2

- [x] T010 [US2] Verify no hardcoded absolute paths exist in src/ — search all .py files for hardcoded paths and replace with relative or runtime-resolved paths
- [ ] T011 [US2] Test portability: copy dist/AutomationMouseKeyboard/ to at least 2 different filesystem locations and verify the app launches from each without errors
- [ ] T012 [US2] Verify the app folder contains all required DLLs and Python runtime — check that no "DLL not found" or "module not found" errors occur on a clean machine

**Checkpoint**: App runs from any folder location — portability verified

---

## Phase 5: User Story 3 - Save and Load Workflows Portably (Priority: P3)

**Goal**: Ensure workflow save/load works correctly in the packaged app, using standard file dialogs and user-chosen locations.

**Independent Test**: Launch packaged app, create a workflow with a few steps, save it to Documents folder, close and reopen app, load the saved workflow, verify all steps are intact.

### Implementation for User Story 3

- [x] T013 [US3] Verify workflow serializer in src/workflow/serializer.py uses no hardcoded paths — confirm save/load uses only the path from file dialog, not relative to app directory
- [ ] T014 [US3] Test workflow round-trip in packaged app: create workflow → save to user-chosen location → close app → reopen → load workflow → verify all steps match
- [ ] T015 [US3] Test workflow sharing: save a workflow from one copy of the app, load it from a different copy in a different location, verify it loads correctly

**Checkpoint**: Workflow save/load works portably across app locations

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and distribution readiness

- [x] T016 [P] Update README.md with instructions for building and distributing the portable app
- [x] T017 [P] Add app name and version to the GUI window title bar in src/gui/app.py (e.g., "Automation Mouse & Keyboard v1.0")
- [ ] T018 Run full quickstart.md validation — follow all steps on a clean Windows machine and confirm end-to-end success

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on T001 (icon) from Setup — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 (build tooling must exist)
- **User Story 2 (Phase 4)**: Depends on Phase 3 (need a working build to test portability)
- **User Story 3 (Phase 5)**: Depends on Phase 3 (need a working build to test workflow save/load)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — no dependencies on other stories
- **User Story 2 (P2)**: Requires US1 complete (needs a working packaged app to test portability)
- **User Story 3 (P3)**: Requires US1 complete (needs a working packaged app to test workflow operations); can run in parallel with US2

### Parallel Opportunities

- T001, T002, T003 in Phase 1 can all run in parallel
- T004, T005 in Phase 2 are sequential (T005 depends on T004)
- T010, T013 (code verification tasks) can run in parallel before building
- T016, T017 in Polish phase can run in parallel
- US2 and US3 can proceed in parallel once US1 is complete

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Create application icon file at assets/app.ico"
Task: "Update .gitignore to exclude dist/ and build/ directories"
Task: "Clean up requirements.txt into runtime and build deps"
```

## Parallel Example: After US1 Complete

```bash
# US2 and US3 can proceed simultaneously:
Task: "T010 [US2] Verify no hardcoded absolute paths in src/"
Task: "T013 [US3] Verify workflow serializer uses no hardcoded paths"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (icon, gitignore, requirements)
2. Complete Phase 2: Foundational (spec file, build script)
3. Complete Phase 3: User Story 1 (error handling, build, test launch)
4. **STOP and VALIDATE**: Double-click .exe on clean Windows machine — app opens with full GUI
5. Ship if ready — this is the core value

### Incremental Delivery

1. Setup + Foundational → Build tooling ready
2. User Story 1 → App launches from .exe → MVP!
3. User Story 2 → Portable across locations → Confidence boost
4. User Story 3 → Workflows save/load portably → Full feature
5. Polish → README, version display, final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The build must happen on a Windows machine (or Windows VM) to produce a Windows .exe
