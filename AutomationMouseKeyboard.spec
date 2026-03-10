# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Automation Mouse & Keyboard portable app.
Builds a one-folder distribution for Windows with no console window.
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# App configuration
app_name = 'AutomationMouseKeyboard'
entry_point = 'src/main.py'
icon_file = 'assets/app.ico'

# Hidden imports - modules PyInstaller can't auto-detect
hidden_imports = [
    # pyautogui and its platform-specific backends
    'pyautogui',
    'pyautogui._pyautogui_osx',
    'pyautogui._pyautogui_win',
    'pyautogui._pyautogui_x11',
    # pynput and its OS-specific listeners
    'pynput',
    'pynput.keyboard',
    'pynput.mouse',
    'pynput._util.win32',
    'pynput._util.win32_vks',
    'pynput._util.xorg',
    # openpyxl and its submodules
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.reader',
    'openpyxl.writer',
    # tkinter (should be auto-detected, but explicit for safety)
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    # Standard library modules used
    'json',
    'threading',
    'queue',
    'logging',
    'datetime',
]

# Collect data files from dependencies
datas = []
try:
    # Collect any data files from openpyxl
    datas += collect_data_files('openpyxl')
except Exception:
    pass

block_cipher = None

a = Analysis(
    [entry_point],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (windowed mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
