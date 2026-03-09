<!--
Sync Impact Report
===================
- Version change: N/A → 1.0.0 (initial ratification)
- Modified principles: N/A (initial creation)
- Added sections:
  - Core Principles (5 principles)
  - Safety & Operational Constraints
  - Development Workflow
  - Governance
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no updates needed (Constitution Check section is generic)
  - .specify/templates/spec-template.md ✅ no updates needed (structure is compatible)
  - .specify/templates/tasks-template.md ✅ no updates needed (phase structure aligns)
- Follow-up TODOs: None
-->

# Automation Mouse & Keyboard Constitution

## Core Principles

### I. Safety First

All automation MUST include fail-safe mechanisms. Every automation
script MUST implement a global kill-switch (e.g., moving the mouse to
a screen corner or pressing a designated hotkey) that immediately
halts execution. Uncontrolled input automation poses real risk of
data loss or unintended system changes. No automation sequence may
run without an active abort mechanism.

### II. Simplicity & Usability

Automation workflows MUST be configurable without modifying source
code. Users MUST be able to define click targets, key sequences,
timing, and data sources through configuration files (YAML, JSON,
or Excel). The barrier to creating a new automation MUST remain low:
a user with basic spreadsheet skills MUST be able to set up and run
a workflow. Avoid abstractions that do not directly serve usability.

### III. Modular Extensibility

Each automation capability (mouse control, keyboard input, Excel
reading, screen detection) MUST be implemented as an independent,
composable module. Adding a new automation type (e.g., image
recognition, clipboard operations) MUST NOT require modifying
existing modules. Modules communicate through well-defined
interfaces, not shared mutable state.

### IV. Data Integrity

When reading from or writing to external data sources (Excel files,
CSVs, clipboard), the system MUST never corrupt the source data.
All write operations MUST target output files or clearly designated
output ranges. The system MUST validate data before acting on it
(e.g., verifying a cell is non-empty before using its value as a
click target). Failed validations MUST halt the automation with a
clear error message rather than proceeding with bad data.

### V. Minimal Critical-Path Testing

Testing effort MUST focus on integration and end-to-end tests for
critical automation paths (click sequences, data-driven workflows,
Excel read/write pipelines). Unit tests are encouraged for utility
functions but are not mandatory. Every new automation module MUST
include at least one integration test demonstrating its primary
use case. Use pytest as the testing framework.

## Safety & Operational Constraints

- **Python stack**: Python 3.10+ with pyautogui (mouse/keyboard),
  openpyxl (Excel), and pynput (input monitoring/kill-switch).
- **Kill-switch hotkey**: MUST be registered before any automation
  begins. Default: `Esc` key. Configurable per-workflow.
- **Timing guards**: All click and type operations MUST include
  configurable delays (minimum 50ms default) to prevent race
  conditions with UI rendering.
- **Dry-run mode**: Every workflow MUST support a dry-run flag that
  logs intended actions without executing them.
- **Logging**: All automation runs MUST produce a timestamped log
  file recording every action taken, enabling post-run audit.

## Development Workflow

- **Branch-per-feature**: All work happens on feature branches
  merged via pull request.
- **Code review**: PRs MUST be reviewed for safety compliance
  (kill-switch present, timing guards in place, no raw
  unguarded input loops).
- **Configuration over code**: New workflows SHOULD be achievable
  by adding/editing config files, not by writing new Python
  scripts. When new code is required, it MUST follow the modular
  extensibility principle.
- **Commit discipline**: Each commit MUST represent a single
  logical change. Commit messages MUST describe the "why."

## Governance

This constitution is the authoritative reference for all design
and implementation decisions in the project. When a proposed change
conflicts with these principles, the constitution takes precedence.

**Amendment procedure**: Any principle change MUST be documented in
a PR with rationale. Breaking changes to principles require a
MAJOR version bump. New principles or material expansions require
a MINOR bump. Clarifications and wording fixes require a PATCH bump.

**Compliance review**: Every PR review MUST include a check that
the change adheres to the Safety First and Data Integrity
principles. The plan template's Constitution Check section MUST
be completed before implementation begins.

**Version**: 1.0.0 | **Ratified**: 2026-03-09 | **Last Amended**: 2026-03-09
