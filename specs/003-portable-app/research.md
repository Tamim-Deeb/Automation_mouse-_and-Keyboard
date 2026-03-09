# Research: Portable App Distribution

**Feature**: 003-portable-app
**Date**: 2026-03-09

## R1: Packaging Tool for Python → Windows Executable

**Decision**: PyInstaller in one-folder mode

**Rationale**: PyInstaller is the most mature and widely-used Python packaging tool. One-folder mode (`--onedir`) produces a directory containing the executable and all dependencies. It supports tkinter, pyautogui, openpyxl, and pynput out of the box (with community hooks). It's already listed in the project's `requirements.txt`.

**Alternatives considered**:
- **PyInstaller one-file mode** (`--onefile`): Bundles everything into a single .exe, but slower startup (must extract to temp dir) and can trigger more aggressive antivirus false positives. Rejected per clarification: user chose folder format.
- **cx_Freeze**: Less community support, fewer hooks for complex dependencies like pyautogui.
- **Nuitka**: Compiles Python to C, good performance but significantly more complex build process and longer build times.
- **py2exe**: Windows-only (which fits), but less actively maintained than PyInstaller.

## R2: Hidden Imports and Hook Requirements

**Decision**: Use `pyinstaller-hooks-contrib` package and declare hidden imports for pyautogui, pynput, and openpyxl submodules

**Rationale**: PyInstaller's static analysis may miss dynamic imports used by pyautogui (platform-specific backends), pynput (OS-specific listeners), and openpyxl (worksheet readers). The `pyinstaller-hooks-contrib` package provides community-maintained hooks that handle most of these. Any remaining missing modules can be added via `--hidden-import` flags in the PyInstaller spec file.

**Alternatives considered**:
- Manual `--hidden-import` for every submodule: error-prone and hard to maintain.
- Runtime import patching: fragile and defeats the purpose of packaging.

## R3: Entry Point Configuration

**Decision**: Use `src/main.py:main()` as the entry point via a PyInstaller `.spec` file

**Rationale**: The app already has a clean `main()` function in `src/main.py`. A `.spec` file gives full control over the build (hidden imports, data files, icon, console window suppression) without long command-line flags.

**Alternatives considered**:
- Command-line PyInstaller invocation: works for simple cases but becomes unwieldy with many options.
- Wrapper script: unnecessary indirection since main.py already serves this purpose.

## R4: Console Window Suppression

**Decision**: Use `--windowed` / `--noconsole` flag to suppress the terminal window on Windows

**Rationale**: Non-technical users should not see a command prompt window behind the GUI app. PyInstaller's `--windowed` flag suppresses this. Error output will be captured via a startup error handler that shows a tkinter messagebox instead.

**Alternatives considered**:
- Leaving console visible: confusing for non-technical users.
- Redirecting stdout/stderr to a log file: good complement (should add), but doesn't address the visible console window.

## R5: Application Icon

**Decision**: Include a custom `.ico` file for the Windows executable

**Rationale**: FR-006 requires a clear app icon in the taskbar. PyInstaller supports `--icon` flag to embed an icon into the executable. An `.ico` file needs to be created or sourced for the project.

**Alternatives considered**:
- No icon (default Python icon): looks unprofessional and doesn't meet FR-006.
- Using a `.png` converted at build time: PyInstaller requires `.ico` format on Windows; conversion adds a build step.

## R6: Build Automation

**Decision**: Create a build script that invokes PyInstaller with the correct configuration

**Rationale**: A reproducible build process ensures anyone can create the portable package. A simple Python or shell script that runs PyInstaller with the `.spec` file is sufficient. No CI/CD pipeline needed (distribution is via direct file sharing per assumptions).

**Alternatives considered**:
- GitHub Actions CI: overhead for a directly-shared app; can be added later if needed.
- Makefile: less portable across developer machines than a Python script.
