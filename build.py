#!/usr/bin/env python3
"""
Build script for Automation Mouse & Keyboard portable Windows app.
Invokes PyInstaller and validates the build output.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
SPEC_FILE = 'AutomationMouseKeyboard.spec'
OUTPUT_DIR = 'dist'
APP_NAME = 'AutomationMouseKeyboard'
EXPECTED_EXE = os.path.join(OUTPUT_DIR, APP_NAME, f'{APP_NAME}.exe')
EXPECTED_INTERNAL = os.path.join(OUTPUT_DIR, APP_NAME, '_internal')


def print_step(message):
    """Print a formatted step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}")


def check_prerequisites():
    """Check if build prerequisites are met."""
    print_step("Checking Prerequisites")
    
    # Check if spec file exists
    if not os.path.exists(SPEC_FILE):
        print(f"✗ ERROR: Spec file '{SPEC_FILE}' not found!")
        return False
    
    # Check if icon exists
    icon_path = 'assets/app.ico'
    if not os.path.exists(icon_path):
        print(f"✗ ERROR: Icon file '{icon_path}' not found!")
        print("  Run 'python create_icon.py' to create it.")
        return False
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ ERROR: PyInstaller not installed!")
        print("  Run: pip install -r requirements-build.txt")
        return False
    
    # Check if entry point exists
    entry_point = 'src/main.py'
    if not os.path.exists(entry_point):
        print(f"✗ ERROR: Entry point '{entry_point}' not found!")
        return False
    
    print("✓ All prerequisites met")
    return True


def clean_build():
    """Clean previous build artifacts."""
    print_step("Cleaning Previous Build")
    
    dirs_to_clean = [OUTPUT_DIR, 'build']
    
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            print(f"  Removing {dir_path}/...")
            shutil.rmtree(dir_path)
    
    print("✓ Build directories cleaned")


def run_pyinstaller():
    """Run PyInstaller with the spec file."""
    print_step("Running PyInstaller")
    
    try:
        # Run PyInstaller
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', SPEC_FILE]
        print(f"  Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,
            text=True
        )
        
        print("✓ PyInstaller completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR: PyInstaller failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ ERROR: Unexpected error running PyInstaller: {e}")
        return False


def validate_build():
    """Validate that the build output is correct."""
    print_step("Validating Build Output")
    
    success = True
    
    # Check if output directory exists
    if not os.path.exists(OUTPUT_DIR):
        print(f"✗ ERROR: Output directory '{OUTPUT_DIR}' not found!")
        return False
    
    # Check if app directory exists
    app_dir = os.path.join(OUTPUT_DIR, APP_NAME)
    if not os.path.exists(app_dir):
        print(f"✗ ERROR: App directory '{app_dir}' not found!")
        return False
    
    print(f"✓ App directory exists: {app_dir}")
    
    # Check if executable exists
    if not os.path.exists(EXPECTED_EXE):
        print(f"✗ ERROR: Executable '{EXPECTED_EXE}' not found!")
        success = False
    else:
        exe_size = os.path.getsize(EXPECTED_EXE)
        print(f"✓ Executable found: {EXPECTED_EXE} ({exe_size:,} bytes)")
    
    # Check if _internal directory exists
    if not os.path.exists(EXPECTED_INTERNAL):
        print(f"✗ ERROR: Internal directory '{EXPECTED_INTERNAL}' not found!")
        success = False
    else:
        # Count items in _internal directory
        internal_items = os.listdir(EXPECTED_INTERNAL)
        print(f"✓ Internal directory found: {EXPECTED_INTERNAL} ({len(internal_items)} items)")
    
    # Check for critical DLLs
    critical_dlls = ['python3', 'tkinter']
    for dll_name in critical_dlls:
        found = any(dll_name.lower() in item.lower() for item in internal_items)
        if found:
            print(f"✓ Critical dependency found: {dll_name}")
        else:
            print(f"⚠ WARNING: Critical dependency may be missing: {dll_name}")
    
    return success


def print_summary(success):
    """Print build summary."""
    print_step("Build Summary")
    
    if success:
        print("✓ BUILD SUCCESSFUL!")
        print(f"\n  Portable app created at: {os.path.join(OUTPUT_DIR, APP_NAME)}")
        print(f"  Executable: {EXPECTED_EXE}")
        print(f"\n  To distribute:")
        print(f"    1. Zip the '{os.path.join(OUTPUT_DIR, APP_NAME)}' folder")
        print(f"    2. Share the zip file with users")
        print(f"    3. Users extract and double-click '{APP_NAME}.exe'")
        return 0
    else:
        print("✗ BUILD FAILED!")
        print("\n  Please check the error messages above and fix any issues.")
        print("  Common issues:")
        print("    - Missing dependencies (run: pip install -r requirements-build.txt)")
        print("    - Missing icon file (run: python create_icon.py)")
        print("    - Entry point not found (check: src/main.py)")
        return 1


def main():
    """Main build function."""
    print("\n" + "="*60)
    print("  Automation Mouse & Keyboard - Build Script")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        return print_summary(False)
    
    # Clean previous build
    clean_build()
    
    # Run PyInstaller
    if not run_pyinstaller():
        return print_summary(False)
    
    # Validate build
    success = validate_build()
    
    # Print summary
    return print_summary(success)


if __name__ == '__main__':
    sys.exit(main())
