# Feature Specification: UI Polish & Visual Enhancement

**Feature Branch**: `017-ui-polish`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Enhance and polish the interface with professional styling, proper window sizing, centered dialogs, colors, and animations. Do not change base functions."

## Clarifications

### Session 2026-03-18

- Q: What overall color direction should the theme follow? → A: Dark header/toolbar with light content panels — professional two-tone look
- Q: How much animation complexity is worth the effort? → A: Step highlight pulse only — flash new step with color on add, skip dialog fade-in and button click animations

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Properly Sized Add Step Dialog (Priority: P1)

When the user clicks "Add Step", the step type selection window currently appears too small and must be manually resized to see all available step types. The dialog MUST open at a size that shows every step type button without scrolling or resizing, and it MUST appear centered on the screen so the user does not need to drag it.

**Why this priority**: This is the most frequently used dialog in the application and the user's primary pain point. Every workflow-building session requires repeated use of this dialog.

**Independent Test**: Click "Add Step" — all 11 step type buttons are visible without scrolling, and the dialog is centered on screen.

**Acceptance Scenarios**:

1. **Given** the main application is open, **When** the user clicks "Add Step", **Then** the Add Step dialog opens centered on the screen with all step type buttons fully visible without any need to scroll or resize.
2. **Given** the Add Step dialog is open, **When** the user selects a step type, **Then** the subsequent Step Editor dialog also opens centered on the screen at an appropriate size for its content.
3. **Given** the application is running on different screen resolutions, **When** any dialog opens, **Then** it appears centered relative to the screen and fits within visible bounds.

---

### User Story 2 - Centered Dialogs for All Pop-Up Windows (Priority: P1)

Every dialog and pop-up window in the application (step editors, confirmations, file dialogs) MUST open centered on the screen. Currently, dialogs appear at unpredictable positions, forcing the user to move them — especially disruptive when picking screen coordinates, as the dialog may cover the target area.

**Why this priority**: Equal to US1 because centering affects every dialog interaction throughout the entire user experience. Reduces friction for coordinate-picking workflows.

**Independent Test**: Open any dialog (Add Step, Step Editor, Delete confirmation, Save/Load, About) — each one appears centered on screen.

**Acceptance Scenarios**:

1. **Given** the main application is open, **When** any dialog opens (Add Step, Step Editor, confirmation, file picker, About), **Then** it appears centered on the user's screen.
2. **Given** the user is building a workflow with coordinate-picking steps, **When** the Step Editor dialog opens after picking, **Then** it returns centered on screen and does not obscure previously selected areas.

---

### User Story 3 - Professional Color Theme & Visual Styling (Priority: P2)

The application MUST have a cohesive, professional two-tone color scheme: a dark header/toolbar area with light content panels. This provides clear visual hierarchy — the dark top section anchors the application identity while light working areas keep content readable. Colors should provide visual hierarchy: accented section headers, styled buttons with hover effects, and clear visual separation between the three main panels (Excel, Workflow, Execution).

**Why this priority**: Visual styling makes the application feel professional and trustworthy. It does not affect functionality but significantly improves perceived quality.

**Independent Test**: Launch the application — the main window displays a dark header with light content panels, styled buttons with hover effects, and clear visual hierarchy between sections.

**Acceptance Scenarios**:

1. **Given** the application launches, **When** the main window appears, **Then** the application displays a dark header/toolbar area with light content panels, and all three panels (Excel Data Source, Workflow Steps, Execution) have clear visual separation.
2. **Given** the main window is displayed, **When** the user hovers over any button, **Then** the button shows a visible hover effect (color change or highlight).
3. **Given** the application is running, **When** the user views the workflow step list, **Then** step items have readable text with proper contrast and visual spacing.
4. **Given** the application is open, **When** the user views panel headers (LabelFrame titles), **Then** they are styled with a distinct accent color and clear typography.

---

### User Story 4 - Step Addition Highlight Animation (Priority: P3)

When the user adds a new step to the workflow list, the newly added step SHOULD briefly flash with a highlight color (color pulse lasting approximately 500ms) before settling to its normal appearance. This draws the user's attention to confirm the step was added successfully. No other animations are included — dialog fade-in and button click effects are excluded to keep implementation lightweight.

**Why this priority**: The step highlight is the single highest-value animation — it gives immediate visual feedback for the most common action. Dialog and button animations add significant effort for marginal perceived improvement.

**Independent Test**: Add a new step to the workflow — the new item appears with a brief highlight flash before settling to its normal row color.

**Acceptance Scenarios**:

1. **Given** a workflow with existing steps, **When** the user adds a new step, **Then** the newly added step briefly highlights (color pulse ~500ms) before settling to its normal appearance.
2. **Given** a step is added that falls under a Condition step's governance, **When** the highlight animation completes, **Then** the step settles to its correct condition color (blue or yellow), not white.

---

### Edge Cases

- What happens when the screen resolution is very small (e.g., 1024x768)? Dialogs MUST clamp their position to remain fully visible within screen bounds.
- What happens when multiple monitors are connected? Dialogs MUST center on the same monitor as the main application window.
- What happens when the workflow list has many steps (30+)? The list MUST remain performant and the color styling MUST not degrade.
- What happens to the existing condition step coloring (blue/yellow)? It MUST be preserved and integrate visually with the new color theme.
- What happens if the user has system-level high-contrast or accessibility settings? The color theme SHOULD NOT override system accessibility preferences.

## Requirements *(mandatory)*

### Functional Requirements

**Dialog Sizing & Positioning**:
- **FR-001**: The Add Step dialog MUST open at a size that displays all step type buttons without scrolling or resizing.
- **FR-002**: All application dialogs (Add Step, Step Editor variants, confirmation dialogs) MUST open centered on the user's screen.
- **FR-003**: All Step Editor dialogs (Click, Type Text, Wait, Condition, Screen Loaded, etc.) MUST open at sizes appropriate for their content — no truncated fields or hidden buttons.
- **FR-004**: Dialog positioning MUST account for screen bounds — no dialog should open partially off-screen.
- **FR-005**: When dialogs open after a coordinate-picking action, they MUST return to center-screen position.

**Color Theme & Styling**:
- **FR-006**: The application MUST apply a two-tone color theme: dark header/toolbar area with light content panels, providing clear visual hierarchy.
- **FR-007**: Buttons MUST display a visible hover effect (color change) when the mouse cursor enters them.
- **FR-008**: The three main panels (Excel, Workflow, Execution) MUST have visually distinct section styling with clear borders or background differentiation.
- **FR-009**: The workflow step listbox MUST have styled items with proper padding, readable font size, and adequate row height.
- **FR-010**: Existing condition step coloring (blue #CCE5FF for equal, yellow #FFFFCC for not-equal) MUST be preserved and remain visually compatible with the new theme.

**Animations**:
- **FR-011**: Newly added workflow steps MUST display a brief highlight animation (color pulse lasting approximately 500ms) to draw the user's attention, then settle to the correct row color.

**Constraints**:
- **FR-012**: No existing functionality MUST be changed — all step types, workflow logic, execution, save/load, and keyboard shortcuts MUST continue to work identically.
- **FR-013**: The application MUST remain responsive during animations — no blocking of user input.
- **FR-014**: Color theme MUST maintain sufficient contrast ratios for text readability (minimum 4.5:1 for normal text per WCAG AA).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The Add Step dialog shows all step type buttons without requiring the user to scroll or resize in 100% of launches.
- **SC-002**: All dialogs open centered on screen within 50 pixels of true center on any screen resolution 1024x768 or larger.
- **SC-003**: All buttons in the application display a visible hover effect when the cursor enters.
- **SC-004**: 100% of existing automated tests continue to pass without modification (no functional regression).
- **SC-005**: The application maintains the same startup time (within 500ms of current) despite added styling.
- **SC-006**: Users can identify all three main panels and their purposes within 3 seconds of viewing the application.
- **SC-007**: New step additions display a visible highlight animation that completes within 1 second.

## Assumptions

- The application uses a standard desktop screen resolution of 1280x720 or higher as the baseline. Smaller resolutions are supported but may show compact layouts.
- The step highlight animation will be lightweight (timer-based color cycling) and will not introduce any noticeable performance overhead.
- The existing condition step coloring (blue/yellow) is considered part of core functionality and will not be altered.
- System accessibility preferences (e.g., high contrast mode) are respected where possible; the custom theme does not override OS-level accessibility settings.
