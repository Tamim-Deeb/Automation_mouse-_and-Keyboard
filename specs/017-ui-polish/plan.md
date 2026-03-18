# Implementation Plan: UI Polish & Visual Enhancement

**Branch**: `017-ui-polish` | **Date**: 2026-03-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/017-ui-polish/spec.md`

## Summary

Enhance the application's visual presentation with a professional two-tone color theme (dark header, light content panels), properly sized and screen-centered dialogs, button hover effects, and a step-addition highlight animation. All changes are purely visual — no existing functionality is modified. Uses ttk.Style with the "clam" theme for full cross-platform color control.

## Technical Context

**Language/Version**: Python 3.10+ (existing)
**Primary Dependencies**: tkinter (stdlib, existing), ttk (stdlib, existing) — no new dependencies
**Storage**: N/A (no new data)
**Testing**: pytest (existing) — visual changes verified manually; existing tests must pass unchanged
**Target Platform**: Windows 10+ (primary), macOS (secondary)
**Project Type**: Desktop application (existing)
**Performance Goals**: Same startup time (within 500ms of current), animations non-blocking
**Constraints**: No new dependencies, no functional changes, WCAG AA contrast (4.5:1 minimum)
**Scale/Scope**: 6 existing GUI files modified, 1 new theme module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Safety First | PASS | No changes to kill-switch, execution, or automation. Visual only. |
| II. Simplicity & Usability | PASS | Improves usability — dialogs properly sized and centered. No new complexity for users. |
| III. Modular Extensibility | PASS | Theme defined in new standalone module (`theme.py`). Other files import from it. No shared mutable state. |
| IV. Data Integrity | PASS | No data operations affected. Read/write paths unchanged. |
| V. Minimal Critical-Path Testing | PASS | No new automation module — no integration test required. Existing tests must pass unchanged. Visual verification is manual. |

**Post-Design Re-check**: All gates still PASS. No new dependencies, no functional changes, theme module follows modular extensibility principle.

## Project Structure

### Documentation (this feature)

```text
specs/017-ui-polish/
├── plan.md              # This file
├── research.md          # Phase 0: tkinter theming research
├── data-model.md        # Phase 1: color palette and dialog sizes
├── quickstart.md        # Phase 1: integration scenario
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── gui/
│   ├── theme.py            # NEW — centralized color palette + ttk.Style setup
│   ├── app.py              # MODIFY — apply theme at startup, style main window
│   ├── step_editors.py     # MODIFY — fix dialog sizes, add centering
│   ├── workflow_panel.py   # MODIFY — step highlight animation, themed listbox
│   ├── excel_panel.py      # MODIFY — apply themed styles
│   └── execution_panel.py  # MODIFY — apply themed styles
└── main.py                 # MODIFY — initialize theme before UI creation

tests/
└── (no changes — existing tests must pass unchanged)
```

**Structure Decision**: Single new file (`src/gui/theme.py`) for theme centralization. All other changes are modifications to existing GUI files. No new test files — this is a visual-only change verified by manual testing and existing test suite regression check.
