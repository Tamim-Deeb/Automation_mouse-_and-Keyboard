"""
Centralized theme module for UI styling and visual enhancements.

This module provides:
- Color palette constants for the application
- Custom ttk styles for widgets
- Dialog centering utility
"""

import tkinter as tk
from tkinter import ttk

# Color Palette Constants
COLOR_DARK_HEADER = "#2b2b2b"        # Dark background for header/toolbar
COLOR_LIGHT_PANEL = "#f5f5f5"        # Light background for content panels
COLOR_BUTTON_BLUE = "#4a90d9"        # Primary button color
COLOR_BUTTON_HOVER = "#357abd"       # Button hover color
COLOR_BUTTON_PRESSED = "#2a5f9e"     # Button pressed color
COLOR_TEXT_DARK = "#333333"          # Dark text for light backgrounds
COLOR_TEXT_LIGHT = "#ffffff"         # Light text for dark backgrounds
COLOR_BORDER_GRAY = "#cccccc"        # Border color
COLOR_HIGHLIGHT_GREEN = "#90EE90"    # Highlight green for new steps
COLOR_WHITE = "#ffffff"              # Pure white
COLOR_CONDITION_EQUAL = "#CCE5FF"    # Blue for equal condition steps
COLOR_CONDITION_NOT_EQUAL = "#FFFFCC" # Yellow for not-equal condition steps


def setup_theme(root):
    """
    Initialize the theme for the application.
    
    Args:
        root: The root Tk window
    """
    # Use the "clam" theme as base
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure custom styles
    _configure_styles(style)
    
    # Apply dark theme to root window
    root.configure(bg=COLOR_DARK_HEADER)


def _configure_styles(style):
    """
    Configure custom ttk styles.
    
    Args:
        style: The ttk.Style instance
    """
    # Dark.TFrame - For header/toolbar areas
    style.configure("Dark.TFrame",
                   background=COLOR_DARK_HEADER)
    
    # Light.TFrame - For content panels
    style.configure("Light.TFrame",
                   background=COLOR_LIGHT_PANEL)
    
    # Custom.TButton - Styled buttons with hover effects
    style.configure("Custom.TButton",
                   background=COLOR_BUTTON_BLUE,
                   foreground=COLOR_TEXT_LIGHT,
                   borderwidth=1,
                   focuscolor="none",
                   padding=(10, 5))
    
    # Button hover state
    style.map("Custom.TButton",
             background=[("active", COLOR_BUTTON_HOVER),
                        ("pressed", COLOR_BUTTON_PRESSED),
                        ("!active", COLOR_BUTTON_BLUE)])
    
    # Styled LabelFrame for panels
    style.configure("Styled.TLabelframe",
                   background=COLOR_LIGHT_PANEL,
                   bordercolor=COLOR_BORDER_GRAY,
                   borderwidth=1)
    
    style.configure("Styled.TLabelframe.Label",
                   background=COLOR_LIGHT_PANEL,
                   foreground=COLOR_TEXT_DARK,
                   font=('TkDefaultFont', 10, 'bold'))


def center_dialog(dialog):
    """
    Center a dialog on the screen with bounds checking.
    
    This function ensures dialogs never open partially off-screen by
    clamping their position within screen bounds.
    
    Args:
        dialog: The Toplevel dialog to center
    """
    # Update dialog to ensure geometry is calculated
    dialog.update_idletasks()
    
    # Get dialog dimensions
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    
    # Get screen dimensions
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    
    # Calculate center position
    x = (screen_width - dialog_width) // 2
    y = (screen_height - dialog_height) // 2
    
    # Clamp position to ensure dialog stays within screen bounds
    x = max(0, min(x, screen_width - dialog_width))
    y = max(0, min(y, screen_height - dialog_height))
    
    # Position the dialog
    dialog.geometry(f"+{x}+{y}")
