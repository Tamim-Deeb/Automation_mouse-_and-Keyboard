# Data Model: Windows Portable Application

**Feature Branch**: `002-windows-exe-packaging`
**Date**: 2026-03-09

## Entities

### Build Configuration

Defines how the application is packaged into an executable.

| Attribute            | Description                                              |
|----------------------|----------------------------------------------------------|
| app_name             | Output executable name: `AutomationBuilder`              |
| entry_point          | Main script: `src/main.py`                               |
| icon_path            | Application icon: `assets/app.ico`                       |
| hidden_imports       | List of modules PyInstaller cannot auto-detect           |
| excludes             | List of unused modules to exclude for size optimization  |
| windowed             | Boolean: suppress console window (true)                  |
| onedir               | Boolean: produce portable folder (true)                  |

### Build Artifact

The output of the build process.

| Attribute     | Description                                      |
|---------------|--------------------------------------------------|
| folder_name   | `AutomationBuilder/`                             |
| exe_name      | `AutomationBuilder.exe` (inside folder)          |
| archive_name  | `AutomationBuilder-windows.zip`                  |
| target_os     | Windows 10+                                      |
| max_size      | 150 MB (unzipped)                                |
| max_startup   | 5 seconds                                        |

### CI Workflow Configuration

Defines the automated build pipeline.

| Attribute       | Description                                       |
|-----------------|---------------------------------------------------|
| trigger_push    | Pushes to `main` branch                           |
| trigger_tag     | Version tags matching `v*.*.*`                     |
| runner          | `windows-latest`                                  |
| python_version  | 3.12                                              |
| artifact_name   | `AutomationBuilder-windows`                       |

## Relationships

- Build Configuration → produces → Build Artifact (portable folder)
- CI Workflow Configuration → triggers → Build Configuration → zips folder → uploads → Build Artifact
- Version tag → triggers → CI Workflow → attaches → `.zip` archive to GitHub Release
