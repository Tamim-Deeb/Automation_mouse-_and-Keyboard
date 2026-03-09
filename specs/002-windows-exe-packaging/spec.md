# Feature Specification: Windows Portable Application

**Feature Branch**: `002-windows-exe-packaging`
**Created**: 2026-03-09
**Status**: Draft
**Input**: User description: "Package the Excel Automation Builder app as a portable Windows folder using PyInstaller. The user unzips a folder and double-clicks the exe inside — no installation or Python required."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build a Portable Windows Application Folder (Priority: P1)

A developer runs a build command on a Windows machine (or via CI) and produces a portable folder containing `AutomationBuilder.exe` and its supporting files. The user unzips the folder anywhere on their Windows machine and double-clicks the exe to launch the app — no installation, no Python, no setup.

**Why this priority**: Without a working build process, no end user can use the app — this is the core deliverable.

**Independent Test**: Run the build script on a clean Windows environment, verify a folder with `AutomationBuilder.exe` is produced, copy the folder to a Windows machine with no Python installed, double-click the exe, and confirm the app launches with all features working.

**Acceptance Scenarios**:

1. **Given** the source code is checked out on a Windows machine with Python installed, **When** the developer runs the build script, **Then** a folder containing `AutomationBuilder.exe` and supporting files is produced in the output directory within 5 minutes.
2. **Given** the portable folder is copied to a Windows machine with no Python installed, **When** the user double-clicks `AutomationBuilder.exe`, **Then** the Excel Automation Builder launches instantly with the full GUI (Excel panel, workflow panel, execution panel).
3. **Given** the app is running from the portable folder, **When** the user imports an Excel file and executes a workflow, **Then** all automation features (mouse, keyboard, wait, kill-switch) function identically to running from source.

---

### User Story 2 - Automated CI Build via GitHub Actions (Priority: P2)

A developer pushes code to the repository and a GitHub Actions workflow automatically builds the portable folder on a Windows runner. The resulting folder is zipped and uploaded as a build artifact that can be downloaded from the Actions tab.

**Why this priority**: Automating the build ensures every release is reproducible and removes the need for a Windows dev machine locally.

**Independent Test**: Push a commit to the main branch, verify the GitHub Actions workflow triggers on a Windows runner, completes successfully, and produces a downloadable `.zip` artifact containing the portable folder.

**Acceptance Scenarios**:

1. **Given** a commit is pushed to the main branch, **When** the GitHub Actions workflow runs, **Then** it builds the portable folder on a Windows runner and uploads it as a `.zip` artifact.
2. **Given** the workflow has completed, **When** a user navigates to the Actions tab, **Then** they can download the `.zip` artifact.
3. **Given** the downloaded `.zip` from CI, **When** extracted and launched on a clean Windows machine, **Then** the app functions identically to a locally built version.

---

### User Story 3 - Release Distribution (Priority: P3)

When a new version is tagged in the repository, the CI workflow automatically attaches the portable folder `.zip` to a GitHub Release so end users can download it from the Releases page.

**Why this priority**: Streamlines distribution but is not required for the app to be usable — users can still get the `.zip` from CI artifacts.

**Independent Test**: Create a Git tag, verify the workflow triggers, builds the portable folder, zips it, and attaches it to a GitHub Release page that is publicly downloadable.

**Acceptance Scenarios**:

1. **Given** a Git tag (e.g., `v1.0.0`) is pushed, **When** the release workflow runs, **Then** the `.zip` is attached to the corresponding GitHub Release.
2. **Given** the release is published, **When** an end user visits the Releases page, **Then** they can download the `.zip` directly.

---

### Edge Cases

- What happens when the build encounters a missing dependency? The build script should fail with a clear error message listing the missing package.
- What happens if the portable folder is run on macOS or Linux? The OS will refuse to run the `.exe` inside — this is expected and acceptable.
- What happens if antivirus software flags the exe? This is a known PyInstaller behavior; the build should be configured to minimize false positives (proper metadata, no unnecessary hidden imports).
- What happens if the user's Windows version is too old? The app targets Windows 10 and later; earlier versions are unsupported.
- What happens if the user moves just the `.exe` out of the folder? The app will fail to start because supporting files are missing — the entire folder must be kept together.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The build process MUST produce a portable folder containing `AutomationBuilder.exe` and all supporting files (dependencies, libraries, data files).
- **FR-002**: The app MUST launch without requiring Python, pip, or any other runtime to be installed on the target machine.
- **FR-003**: The folder MUST bundle all required dependencies: tkinter, pyautogui, openpyxl, pynput, and their transitive dependencies.
- **FR-004**: The main executable MUST be named `AutomationBuilder.exe`.
- **FR-005**: The app MUST display a custom application icon in the taskbar and window title bar.
- **FR-006**: A build script MUST exist that developers can run with a single command to produce the portable folder.
- **FR-007**: A GitHub Actions workflow MUST build the portable folder on a Windows runner, zip it, and upload it as a downloadable artifact, triggered on pushes to the main branch and version tags.
- **FR-008**: The app MUST support Windows 10 and later.
- **FR-009**: The portable folder (unzipped) MUST be under 150 MB to remain practical for distribution.
- **FR-010**: The application MUST start within 5 seconds of double-clicking the exe (no extraction delay since files are already unpacked).
- **FR-011**: The app MUST run as a windowed application with no console window visible to the user.
- **FR-012**: The build process MUST be reproducible — running the same build script on the same source code MUST produce a functionally identical output.

### Key Entities

- **Build Configuration**: Defines how the application is packaged — included files, icon, name, bundled dependencies, and output settings.
- **Build Artifact**: The resulting portable folder (and its `.zip` archive) produced by the build process, ready for distribution.
- **CI Workflow**: The automated pipeline that builds the portable folder on push/tag events and publishes artifacts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A non-technical user can download the `.zip`, extract it, and launch the application on a clean Windows 10+ machine in under 2 minutes.
- **SC-002**: The build script produces the portable folder in under 5 minutes on a standard CI runner.
- **SC-003**: 100% of application features available when running from source are also functional in the portable build.
- **SC-004**: The portable folder (unzipped) is under 150 MB.
- **SC-005**: The CI workflow succeeds on every push to the main branch without manual intervention.
- **SC-006**: The app starts within 5 seconds of double-clicking (faster than single-file mode).

## Clarifications

### Session 2026-03-09

- Q: What should the executable file be named? → A: AutomationBuilder.exe
- Q: Should the exe show a console window? → A: Windowed only, no console window visible
- Q: When should CI build the exe? → A: Pushes to main branch only (plus tags for releases)
- Q: Single-file exe or portable folder? → A: Portable folder (user unzips and runs, faster startup, fewer AV issues)

## Assumptions

- PyInstaller is the packaging tool (industry standard for Python to Windows exe), using `--onedir` mode.
- The application icon will be provided as an `.ico` file in the repository.
- GitHub Actions free tier provides sufficient Windows runner minutes for CI builds.
- End users are on Windows 10 or later (Windows 7/8 are not supported).
- Code signing is out of scope for this feature (can be added later to reduce antivirus false positives).
- The portable folder will be distributed as a `.zip` archive.
