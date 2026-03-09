# Feature Specification: Portable App Distribution

**Feature Branch**: `003-portable-app`
**Created**: 2026-03-09
**Status**: Draft
**Input**: User description: "Make the app available for users by just opening it, no installing required"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Launch App Without Installation (Priority: P1)

A non-technical user receives the app (e.g., downloads it or gets it from a colleague). They open it directly — no need to install Python, run terminal commands, or set up dependencies. The app launches with its full GUI and all features work immediately.

**Why this priority**: This is the core value of the feature. Without this, non-programmers cannot use the app at all.

**Independent Test**: Can be tested by giving the packaged app to someone who has never installed Python and verifying the app opens and displays the main window.

**Acceptance Scenarios**:

1. **Given** a user with no programming tools installed, **When** they open the app file, **Then** the application launches and displays the main GUI window within 10 seconds
2. **Given** a user opens the app for the first time, **When** the app starts, **Then** no installation wizard, terminal window, or setup steps appear
3. **Given** a user on a supported operating system, **When** they open the app, **Then** all features (workflow builder, mouse/keyboard automation, Excel reading, action logging) function correctly

---

### User Story 2 - Download and Run from a Single File or Folder (Priority: P2)

A user downloads the app as a single self-contained folder. They do not need to download additional files, libraries, or runtimes separately. Everything needed is bundled within the folder, and the user opens the executable inside it.

**Why this priority**: Simplicity of distribution is key — if users need to gather multiple files or install runtimes, the "no install" promise breaks down.

**Independent Test**: Can be tested by copying the packaged app to a clean machine and verifying it runs without downloading anything else.

**Acceptance Scenarios**:

1. **Given** the distributed app package, **When** a user copies it to any location on their computer, **Then** it runs from that location without errors
2. **Given** a user moves the app to a different folder, **When** they open it from the new location, **Then** it still works correctly
3. **Given** the app package, **When** checking its contents, **Then** all required dependencies are bundled within

---

### User Story 3 - Save and Load Workflows Portably (Priority: P3)

A user creates automation workflows in the app and saves them. The saved workflow files work regardless of where the app is located on the computer. Users can share workflow files with other users who have the app.

**Why this priority**: Workflows are the main output of the app — users need confidence their work is saved and shareable.

**Independent Test**: Can be tested by creating a workflow, saving it, moving the app, and reopening the workflow.

**Acceptance Scenarios**:

1. **Given** a user has created a workflow, **When** they save it, **Then** the workflow file is saved to a user-chosen location (not locked inside the app folder)
2. **Given** a saved workflow file, **When** another user with the app opens it, **Then** the workflow loads correctly with all steps intact

---

### Edge Cases

- What happens when the user's operating system blocks the app from running (security/permissions)?
- What happens when the user tries to run the app from a read-only location (e.g., a USB drive with write protection)?
- How does the app behave if the user's screen resolution is very small or very large?
- What happens if a user tries to open a workflow file created with a different version of the app?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The app MUST launch as a standalone application without requiring users to install any programming languages, package managers, or dependencies
- **FR-002**: The app MUST be distributed as a single self-contained folder containing the executable and all its dependencies
- **FR-003**: The app MUST display the full GUI with all existing features (workflow builder, automation controls, Excel panel, execution panel) when launched
- **FR-004**: The app MUST work when placed in any directory on the user's file system
- **FR-005**: The app MUST save and load workflow files using standard file dialogs, with files stored in user-chosen locations
- **FR-006**: The app MUST provide a clear app icon and name visible in the operating system's taskbar/dock
- **FR-007**: The app MUST show a user-friendly error message if something goes wrong at startup, rather than a technical crash trace
- **FR-008**: The app MUST support Windows as the target operating system

### Key Entities

- **App Package**: A self-contained folder containing the executable and all its dependencies, ready to run
- **Workflow File**: A saved automation workflow that users create, store, and share independently of the app location

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A non-technical user can go from receiving the app to having it running in under 30 seconds (no install steps)
- **SC-002**: 100% of existing app features work identically in the portable version as they do when running from source
- **SC-003**: The app launches successfully on a clean machine (no development tools installed) on the first attempt
- **SC-004**: Users can share the app package with others and those recipients can run it without any additional setup

## Clarifications

### Session 2026-03-09

- Q: Package format — single file or single folder? → A: Single folder containing the executable and dependencies
- Q: Windows SmartScreen security warnings — code sign or not? → A: No code signing; users may see a one-time warning they can dismiss

## Assumptions

- The app will be distributed via direct file sharing (e.g., download link, email, USB drive) rather than through an app store
- Users have standard operating system permissions (not restricted enterprise lockdown environments)
- The app is not code-signed; users may encounter a one-time Windows SmartScreen warning which they can dismiss by clicking "Run anyway"
- The existing app functionality (GUI, automation, Excel reading) is stable and working correctly before packaging
- Workflow files use a portable format (e.g., JSON) that does not depend on absolute file paths
