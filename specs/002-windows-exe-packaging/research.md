# Research: Windows Executable Packaging

**Feature Branch**: `002-windows-exe-packaging`
**Date**: 2026-03-09

## 1. PyInstaller Portable Folder Mode

**Decision**: Use `--onedir --windowed --name AutomationBuilder --icon assets/app.ico`

**Rationale**: `--onedir` (the default) produces a folder with the exe and all supporting files alongside it. No temp extraction needed — the app starts instantly. `--windowed` suppresses the console window. Distribute the folder as a `.zip` archive. Fewer antivirus false positives than `--onefile` since there's no suspicious temp extraction behavior.

**Alternatives considered**:
- `--onefile`: Single exe but slower startup (2-10s extraction), more AV false positives — rejected by user preference.
- Nuitka: Compiles to native C, fewer AV false positives, but more complex build and longer build times — overkill for this project.

## 2. Hidden Imports

**Decision**: Explicitly declare hidden imports in the `.spec` file:
- `pynput.keyboard._win32`, `pynput.mouse._win32` (platform-specific backends)
- `pygetwindow`, `pymsgbox`, `pytweening`, `pyscreeze`, `mouseinfo` (pyautogui sub-dependencies)
- `et_xmlfile` (openpyxl dependency)

**Rationale**: These libraries use dynamic imports (`importlib.import_module()`) that PyInstaller's static analysis cannot detect. The pynput `_win32` modules are the most common failure point.

**Alternatives considered**:
- `--collect-all <package>`: Brute-force inclusion of all package files — works but inflates binary size unnecessarily.
- Community hooks via `pyinstaller-hooks-contrib`: Should be installed as a safety net but explicit hidden imports are more reliable.

## 3. Build Configuration Format

**Decision**: Use a committed `.spec` file (e.g., `build/AutomationBuilder.spec`)

**Rationale**: A `.spec` file is a Python script providing full reproducible control over hidden imports, excludes, data files, and platform logic. CLI args become unwieldy with 6+ hidden imports and excludes.

**Alternatives considered**:
- CLI flags only: Fine for simple apps but not maintainable at this complexity.
- Makefile wrapping CLI: Middle ground but `.spec` is the PyInstaller-idiomatic approach.

## 4. GitHub Actions Setup

**Decision**: Use `windows-latest` runner with Python 3.12 via `actions/setup-python@v5`

**Rationale**: `windows-latest` (Windows Server 2022) has Visual C++ runtimes pre-installed. The `setup-python` action provides official CPython builds that include tkinter. Python 3.12 has mature PyInstaller support.

**Key gotchas**:
- No display server (headless) — GUI init must be behind `if __name__ == '__main__'` (already the case in our app).
- tkinter is included in `actions/setup-python` CPython builds but NOT in conda/pyenv builds.

**Alternatives considered**:
- Self-hosted runner: Needed for code signing but out of scope.
- Cross-compilation from Linux via Wine: Fragile, not recommended.

## 5. Antivirus False Positives

**Decision**: Build PyInstaller bootloader from source, avoid UPX compression, accept some false positives without code signing.

**Rationale**: PyInstaller's shared bootloader signature is in many AV databases. Building from source changes the binary signature. UPX compression worsens false positives. Code signing ($200-400/year EV certificate) is out of scope per spec assumptions.

**Alternatives considered**:
- Code signing with EV certificate: Best solution but costs money — deferred.
- MSIX packaging via Windows Store: Provides trust but requires Microsoft developer account — out of scope.

## 6. File Size Optimization

**Decision**: Exclude unused stdlib modules, use clean virtual environment, avoid UPX. Target: 50-70MB.

**Rationale**: Estimated baseline without optimization is 40-60MB. Excluding unused modules (matplotlib, numpy, pytest, setuptools, unittest, etc.) saves 10-20MB. A clean venv prevents development dependencies from being bundled.

**Alternatives considered**:
- UPX compression: 30-40% size reduction but increases AV false positives — rejected.
- `--onefile`: Single file but larger and slower startup — rejected by user preference.
