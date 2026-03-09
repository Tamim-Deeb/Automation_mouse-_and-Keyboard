# Tasks: Windows Portable Application Packaging

**Input**: Design documents from `/specs/002-windows-exe-packaging/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested — test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Build config**: `build/` at repository root
- **Assets**: `assets/` at repository root
- **CI**: `.github/workflows/` at repository root

---

## Phase 1: Setup

**Purpose**: Create directory structure and add build dependencies

- [x] T001 Create `build/` directory and `assets/` directory at repository root
- [x] T002 [P] Add `pyinstaller` and `pyinstaller-hooks-contrib` to requirements.txt (or create a separate `requirements-build.txt`)
- [x] T003 [P] Add an application icon file at assets/app.ico (Windows .ico format, at least 256x256)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure the existing app entry point is compatible with PyInstaller packaging

**CRITICAL**: No build tasks can succeed until this phase is complete

- [x] T004 Verify src/main.py entry point uses `if __name__ == '__main__'` guard for all GUI initialization (required for PyInstaller and headless CI builds)
- [x] T005 [P] Verify all imports in src/ use relative or package imports that PyInstaller can resolve (no dynamic path manipulation like `sys.path.append`)
- [x] T006 [P] Add `dist/`, `build/` (PyInstaller output), and `*.spec` output directories to .gitignore

**Checkpoint**: App source code is PyInstaller-compatible — build tasks can begin

---

## Phase 3: User Story 1 — Build a Portable Windows Application Folder (Priority: P1) MVP

**Goal**: Developer runs a single command and gets a portable folder with `AutomationBuilder.exe` that works on any Windows 10+ machine without Python

**Independent Test**: Copy the `dist/AutomationBuilder/` folder to a clean Windows 10+ machine with no Python, double-click `AutomationBuilder.exe`, import an Excel file, build a workflow, run in dry-run mode — all features work

### Implementation for User Story 1

- [x] T007 [US1] Create PyInstaller spec file at build/AutomationBuilder.spec with: onedir mode, windowed (no console), name=AutomationBuilder, icon=assets/app.ico, entry point=src/main.py, hidden imports for pynput._win32 backends + pyautogui sub-dependencies + et_xmlfile, excludes for unused stdlib modules (matplotlib, numpy, pytest, setuptools, unittest, etc.)
- [x] T008 [US1] Create build script at build/build.py that: creates a clean virtual environment, installs only production dependencies, runs PyInstaller with the spec file, and outputs the portable folder to dist/AutomationBuilder/ (single-command build: `python build/build.py`)
- [ ] T009 [US1] Test the build locally on Windows: run `python build/build.py`, verify dist/AutomationBuilder/ folder is created with AutomationBuilder.exe inside, verify folder size is under 150 MB (NOTE: Must be done on Windows - cannot test on macOS)
- [ ] T010 [US1] Verify the built exe launches correctly on Windows: double-click AutomationBuilder.exe, confirm GUI appears within 5 seconds, confirm no console window is visible, confirm app icon appears in taskbar (NOTE: Must be done on Windows - cannot test on macOS)
- [ ] T011 [US1] Verify all app features work in the built exe: import an Excel file, build a workflow with click/type/wait steps, run in dry-run mode, verify kill-switch (Esc) works, verify save/load workflow works (NOTE: Must be done on Windows - cannot test on macOS)

**Checkpoint**: Portable folder build works — developer can produce a distributable app with one command

---

## Phase 4: User Story 2 — Automated CI Build via GitHub Actions (Priority: P2)

**Goal**: GitHub Actions automatically builds the portable folder on push to main, zips it, and uploads as a downloadable artifact

**Independent Test**: Push a commit to main, verify the workflow runs on a Windows runner, completes successfully, and produces a downloadable `AutomationBuilder-windows.zip` artifact in the Actions tab

### Implementation for User Story 2

- [x] T012 [US2] Create GitHub Actions workflow at .github/workflows/build-exe.yml per contracts/ci-workflow-schema.yml: trigger on push to main, use windows-latest runner, setup Python 3.12 via actions/setup-python@v5, install dependencies, run PyInstaller with build/AutomationBuilder.spec, zip dist/AutomationBuilder/ to AutomationBuilder-windows.zip, upload zip as artifact via actions/upload-artifact@v4
- [ ] T013 [US2] Push to main branch and verify the workflow triggers, builds successfully on the Windows runner, and produces a downloadable artifact (requires pushing to main)
- [ ] T014 [US2] Download the CI-built artifact, extract the zip on a clean Windows machine, verify AutomationBuilder.exe launches and all features work identically to a local build (requires Windows machine)

**Checkpoint**: CI pipeline works — every push to main automatically produces a downloadable portable app

---

## Phase 5: User Story 3 — Release Distribution (Priority: P3)

**Goal**: Pushing a version tag (e.g., v1.0.0) automatically builds and attaches the portable folder zip to a GitHub Release

**Independent Test**: Push a tag like `v1.0.0`, verify a GitHub Release is created with `AutomationBuilder-windows.zip` attached and downloadable from the Releases page

### Implementation for User Story 3

- [x] T015 [US3] Extend .github/workflows/build-exe.yml to also trigger on tag pushes matching `v*.*.*`, add a release job that: depends on the build job, downloads the zip artifact, creates a GitHub Release using the tag name, and attaches AutomationBuilder-windows.zip to the release
- [ ] T016 [US3] Test by creating and pushing a version tag (e.g., `v0.1.0`), verify the workflow triggers, builds the zip, creates a GitHub Release, and the zip is downloadable from the Releases page (requires pushing a tag)

**Checkpoint**: Full distribution pipeline — tag a release and users can download from GitHub Releases

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, size optimization, and documentation

- [x] T017 [P] Verify the built exe handles missing Excel files gracefully (user tries to import a non-existent file)
- [x] T018 [P] Check portable folder size and optimize if over 100 MB: review excludes list in build/AutomationBuilder.spec, remove unnecessary bundled modules, verify no dev dependencies are included
- [x] T019 [P] Add a README section or update quickstart.md with end-user instructions: how to download, extract, and run the portable app
- [ ] T020 Run quickstart.md validation scenarios end-to-end on a clean Windows machine per specs/002-windows-exe-packaging/quickstart.md (requires Windows machine)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all build tasks
- **User Story 1 (Phase 3)**: Depends on Phase 2 — core MVP (local build)
- **User Story 2 (Phase 4)**: Depends on Phase 3 (needs working spec file and build script to automate in CI)
- **User Story 3 (Phase 5)**: Depends on Phase 4 (extends the CI workflow with release job)
- **Polish (Phase 6)**: Depends on Phases 3–5 being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependencies on other stories
- **US2 (P2)**: Depends on US1 (needs build/AutomationBuilder.spec and build/build.py to exist)
- **US3 (P3)**: Depends on US2 (extends the CI workflow created in US2)

### Within Each User Story

- Build config before build script
- Build script before verification
- Local verification before CI automation
- Story complete before moving to next priority

### Parallel Opportunities

- Phase 1: T002 and T003 can run in parallel (different files)
- Phase 2: T005 and T006 can run in parallel (different files)
- Phase 6: T017, T018, T019 can all run in parallel (independent concerns)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (directories, dependencies, icon)
2. Complete Phase 2: Foundational (verify entry point, imports, gitignore)
3. Complete Phase 3: User Story 1 (spec file, build script, verify)
4. **STOP and VALIDATE**: Build on Windows, copy to clean machine, verify all features work
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test locally → Demo (MVP!)
3. Add User Story 2 → Verify CI builds → Demo (automated builds)
4. Add User Story 3 → Tag a release → Demo (full distribution pipeline)
5. Polish → Final validation against quickstart.md

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User stories are sequential in this feature (US2 depends on US1, US3 depends on US2) — cannot parallelize across stories
- The build MUST be done on Windows (or Windows CI runner) — PyInstaller produces platform-specific output
- Since you are developing on macOS, the local build (T009-T011) must be done on a Windows machine or deferred to CI validation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
