"""Preferences persistence for application settings."""

import json
import os
from pathlib import Path
from typing import Dict, Any


def _get_preferences_path() -> Path:
    """Get the path to the preferences file."""
    return Path.home() / ".automation-mouse" / "preferences.json"


def _get_default_preferences() -> Dict[str, Any]:
    """Get default preferences values."""
    return {"step_delay_ms": 200}


def load_preferences() -> Dict[str, Any]:
    """
    Load user preferences from the preferences file.
    
    Returns:
        Dictionary containing loaded preferences with defaults applied.
        If the file is missing or corrupted, returns default preferences.
    """
    prefs_path = _get_preferences_path()
    default_prefs = _get_default_preferences()
    
    if not prefs_path.exists():
        return default_prefs.copy()
    
    try:
        with open(prefs_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        
        # Merge with defaults, ignoring unknown keys for forward compatibility
        result = default_prefs.copy()
        for key, value in loaded.items():
            if key in result:
                result[key] = value
        
        return result
    except (json.JSONDecodeError, IOError, OSError):
        # File corrupted or unreadable - return defaults
        return default_prefs.copy()


def save_preferences(prefs: Dict[str, Any]) -> None:
    """
    Save user preferences to the preferences file.
    
    Args:
        prefs: Dictionary of preferences to save. Only known keys are saved.
    
    Raises:
        OSError: If the preferences directory cannot be created or file cannot be written.
    """
    prefs_path = _get_preferences_path()
    default_prefs = _get_default_preferences()
    
    # Create directory if it doesn't exist
    prefs_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Filter to only known keys for forward compatibility
    filtered_prefs = {k: v for k, v in prefs.items() if k in default_prefs}
    
    with open(prefs_path, "w", encoding="utf-8") as f:
        json.dump(filtered_prefs, f, indent=2)
