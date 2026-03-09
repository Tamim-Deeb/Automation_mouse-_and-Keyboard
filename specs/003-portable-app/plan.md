# Implementation Plan: Portable App Distribution

**Branch**: `003-portable-app` | **Date**: 2026-03-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-portable-app/spec.md`

## Summary

Package the existing Python/tkinter automation app into a self-contained Windows folder using PyInstaller (one-folder mode). Users will double-click the `.exe` to launch the full GUI with no installation required. The build produces a portable folder containing the executable and all bundled dependencies.

## Technical Context

**Language/Version**: Python 3.10+ (existing), Python 3.12 recommended for build
**Primary Dependencies**: PyInstaller 6.0+ (build tool), pyinstaller-hooks-contrib (community hooks)
**Storage**: N/A (packaging feature, no new storage)
**Testing**: pytest (existing); manual testing on clean Windows machine for packaging validation
**Target Platform**: Windows 10/11
**Project Type**: Desktop app (existing) → portable desktop app (this feature)
**Performance Goals**: App launches within 10 seconds from packaged executable
**Constraints**: No code signing; folder-based distribution; no installer wizard
**Scale/Scope**: Single app, single platform (Windows)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch and abort mechanisms are preserved — packaging does not alter runtime behavior |
| II. Simplicity & Usability | PASS | This feature directly serves usability by removing the Python install barrier |
| III. Modular Extensibility | PASS | No changes to module architecture; packaging wraps existing modules |
| IV. Data Integrity | PASS | No changes to data handling; workflow save/load uses user-chosen paths |
| V. Minimal Critical-Path Testing | PASS | Integration test needed: verify packaged app launches and core features work |

**Post-Phase 1 Re-check**: All principles still satisfied. The build configuration is additive (new files only), no existing modules modified.

## Project Structure

### Documentation (this feature)

```text
specs/003-portable-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── build-spec-contract.md
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── main.py              # Entry point (add frozen-app error handling)
├── gui/                 # Existing GUI modules (unchanged)
├── automation/          # Existing automation modules (unchanged)
├── engine/              # Existing engine modules (unchanged)
├── excel/               # Existing Excel modules (unchanged)
├── workflow/            # Existing workflow modules (unchanged)
└── action_logging/      # Existing logging modules (unchanged)

build.py                 # NEW: Build script that invokes PyInstaller
AutomationMouseKeyboard.spec  # NEW: PyInstaller spec file
assets/
└── app.ico              # NEW: Application icon for Windows executable

tests/
└── integration/
    └── test_build.py    # NEW: Verify build produces working executable

dist/                    # BUILD OUTPUT (gitignored)
└── AutomationMouseKeyboard/
    ├── AutomationMouseKeyboard.exe
    └── _internal/
```

**Structure Decision**: Existing `src/` structure preserved. New files added at repo root (`build.py`, `.spec` file) and `assets/` directory for the icon. Build output goes to `dist/` (gitignored).

## Complexity Tracking

No constitution violations — no entries needed.
