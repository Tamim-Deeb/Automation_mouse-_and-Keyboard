"""Coordinate picker overlay for capturing screen coordinates"""
import tkinter as tk
from typing import Optional, Callable


class CoordinatePicker:
    """
    Transparent fullscreen overlay for capturing screen coordinates.
    User clicks anywhere on screen to capture coordinates.
    Press Esc to cancel.
    """
    
    def __init__(self, parent: tk.Tk, on_coords_captured: Callable[[int, int], None]):
        """
        Initialize the coordinate picker.
        
        Args:
            parent: Parent window
            on_coords_captured: Callback when coordinates are captured (receives x, y)
        """
        self.parent = parent
        self.on_coords_captured = on_coords_captured
        
        self.overlay: Optional[tk.Toplevel] = None
        self.captured_coords: Optional[tuple[int, int]] = None
    
    def pick(self) -> None:
        """Show the coordinate picker overlay"""
        # Create fullscreen overlay window
        self.overlay = tk.Toplevel(self.parent)
        
        # Make it fullscreen and transparent
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-alpha', 0.3)  # Semi-transparent
        self.overlay.configure(bg='gray')
        
        # Remove window decorations
        self.overlay.overrideredirect(True)
        
        # Capture mouse clicks
        self.overlay.bind('<Button-1>', self._on_click)
        
        # Capture Esc key to cancel
        self.overlay.bind('<Escape>', self._on_cancel)
        
        # Add instructions
        label = tk.Label(
            self.overlay,
            text="Click anywhere to capture coordinates\nPress Esc to cancel",
            bg='gray',
            fg='white',
            font=('Arial', 14, 'bold')
        )
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Make overlay modal
        self.overlay.transient(self.parent)
        self.overlay.grab_set()
    
    def _on_click(self, event) -> None:
        """
        Handle mouse click on overlay.
        
        Args:
            event: Mouse event containing coordinates
        """
        # Capture coordinates
        self.captured_coords = (event.x, event.y)
        
        # Close overlay
        self._close()
        
        # Notify callback
        if self.on_coords_captured:
            self.on_coords_captured(self.captured_coords[0], self.captured_coords[1])
    
    def _on_cancel(self, event) -> None:
        """Handle Esc key press to cancel"""
        self.captured_coords = None
        self._close()
    
    def _close(self) -> None:
        """Close the overlay window"""
        if self.overlay:
            try:
                self.overlay.destroy()
            except tk.TclError:
                pass
            self.overlay = None
    
    def is_active(self) -> bool:
        """
        Check if the picker is currently active.
        
        Returns:
            True if picker is active, False otherwise
        """
        return self.overlay is not None
