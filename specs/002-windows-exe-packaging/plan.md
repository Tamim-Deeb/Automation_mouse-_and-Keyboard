# Implementation Plan: Windows Executable Packaging

**Branch**: `002-windows-exe-packaging` | **Date**: 2026-03-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-windows-exe-packaging/spec.md`

## Summary

Package the Excel Automation Builder as a portable Windows folder using PyInstaller `--onedir` mode with a committed `.spec` file. The user unzips a folder and double-clicks `AutomationBuilder.exe` — no installation or Python required. Automate the build via GitHub Actions on a Windows runner, triggered on pushes to main and version tags. The app runs windowed (no console), bundles all dependencies, and targets Windows 10+. Distributed as a `.zip` archive.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: PyInstaller (build tool), pyinstaller-hooks-contrib (community hooks)
**Storage**: N/A (build/packaging feature)
**Testing**: Manual verification on Windows; CI workflow validation via GitHub Actions
**Target Platform**: Windows 10+ (build runs on GitHub Actions `windows-latest`)
**Project Type**: Build/packaging toolchain for existing desktop app
**Performance Goals**: Exe startup < 5 seconds (no extraction needed), build time < 5 minutes on CI
**Constraints**: Portable folder < 150 MB unzipped, no console window, no code signing (deferred)
**Scale/Scope**: Single artifact output

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | Kill-switch and fail-safes are in the existing app code — packaging preserves them unchanged. |
| II. Simplicity & Usability | PASS | End users double-click a single file — maximum simplicity. No config needed to run. |
| III. Modular Extensibility | PASS | Build config is a separate `.spec` file; CI workflow is independent YAML. Neither modifies existing app modules. |
| IV. Data Integrity | PASS | Packaging does not touch Excel files or data sources. Read-only bundling of source code. |
| V. Minimal Critical-Path Testing | PASS | Manual verification of the built exe covers the critical path. CI workflow validates reproducibility. |

**Post-Phase 1 re-check**: All gates still PASS. No design decisions violate constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/002-windows-exe-packaging/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── ci-workflow-schema.yml
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
build/
├── AutomationBuilder.spec   # PyInstaller spec file
└── build.py                 # Build script wrapper (single-command build)

assets/
└── app.ico                  # Application icon

.github/
└── workflows/
    └── build-exe.yml        # GitHub Actions workflow

src/                         # Existing app code (unchanged)
tests/                       # Existing tests (unchanged)
```

**Structure Decision**: Build configuration lives in `build/` at the repository root, separate from application source. The `.github/workflows/` directory follows GitHub convention. An `assets/` directory holds the application icon.

## Complexity Tracking

No constitution violations — this section is not needed.
