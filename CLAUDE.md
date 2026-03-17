# Automation_mouse-_and-Keyboard Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-09

## Active Technologies
- Python 3.10+ + tkinter (GUI, stdlib), pyautogui (mouse/keyboard) (001-excel-automation-builder)
- Python 3.10+ (existing), Python 3.12 recommended for build + PyInstaller 6.0+ (build tool), pyinstaller-hooks-contrib (community hooks) (003-portable-app)
- N/A (packaging feature, no new storage) (003-portable-app)
- Python 3.10+ + pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel) (009-safe-stop)
- N/A (no new storage) (009-safe-stop)
- Python 3.10+ (existing) + pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel) (010-default-step-delay)
- JSON preferences file (~/.automation-mouse/preferences.json) for delay persistence (010-default-step-delay)
- Python 3.10+ (existing) + pyautogui (keyboard automation), pyperclip (clipboard clearing), tkinter (GUI) (011-copy-field-step)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.10+: Follow standard conventions

## Recent Changes
- 011-copy-field-step: Added Python 3.10+ (existing) + pyautogui (keyboard automation), pyperclip (clipboard clearing), tkinter (GUI)
- 010-default-step-delay: Added Python 3.10+ (existing) + pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel)
- 009-safe-stop: Added Python 3.10+ + pyautogui (mouse/keyboard), pynput (kill-switch listener), tkinter (GUI), openpyxl (Excel)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
