"""Coordinate picker for capturing screen coordinates"""
import tkinter as tk
from typing import Optional, Callable
import pyautogui


class CoordinatePicker:
    """
    Lightweight coordinate picker.
    Shows a small floating window — user moves mouse to desired position
    and presses Enter (or clicks the Capture button) to grab coordinates.
    Press Esc to cancel.
    """

    def __init__(self, parent: tk.Tk, on_coords_captured: Callable[[int, int], None]):
        self.parent = parent
        self.on_coords_captured = on_coords_captured

        self._window: Optional[tk.Toplevel] = None
        self._coord_label: Optional[tk.Label] = None
        self.captured_coords: Optional[tuple[int, int]] = None
        self._polling_id: Optional[str] = None

    def pick(self) -> None:
        """Show the coordinate picker"""
        self._window = tk.Toplevel(self.parent)
        self._window.title("Pick Coordinates")
        self._window.overrideredirect(True)
        self._window.attributes('-topmost', True)
        self._window.configure(bg='#222222')

        frame = tk.Frame(self._window, bg='#222222', padx=10, pady=8)
        frame.pack()

        tk.Label(
            frame,
            text="Move mouse to target, then press Enter  |  Esc to cancel",
            bg='#222222', fg='white',
            font=('Arial', 12, 'bold'),
        ).pack()

        self._coord_label = tk.Label(
            frame,
            text="X: 0   Y: 0",
            bg='#222222', fg='#00ff88',
            font=('Courier', 14, 'bold'),
        )
        self._coord_label.pack(pady=(4, 6))

        btn_frame = tk.Frame(frame, bg='#222222')
        btn_frame.pack()

        tk.Button(
            btn_frame, text="Capture", command=self._capture,
            bg='#444444', fg='white', font=('Arial', 11),
            relief='flat', padx=12, pady=2,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            btn_frame, text="Cancel", command=self._cancel,
            bg='#444444', fg='white', font=('Arial', 11),
            relief='flat', padx=12, pady=2,
        ).pack(side=tk.LEFT, padx=4)

        # Position at top-center
        self._window.update_idletasks()
        w = self._window.winfo_width()
        sw = self._window.winfo_screenwidth()
        self._window.geometry(f"+{(sw - w) // 2}+30")

        # Key bindings
        self._window.bind('<Return>', lambda e: self._capture())
        self._window.bind('<Escape>', lambda e: self._cancel())

        # Grab all keyboard input so Enter/Esc work even when mouse is elsewhere
        self._window.grab_set_global()
        self._window.focus_force()

        # Start polling mouse position and maintaining focus
        self._poll_mouse()

    def _poll_mouse(self) -> None:
        """Update the displayed coordinates with current mouse position"""
        if self._window is None:
            return
        try:
            x, y = pyautogui.position()
            self._coord_label.config(text=f"X: {x}   Y: {y}")
            # Re-focus periodically so Windows doesn't steal keyboard input
            self._window.focus_force()
            self._polling_id = self._window.after(50, self._poll_mouse)
        except Exception:
            pass

    def _capture(self) -> None:
        """Capture current mouse position"""
        if self._window is None:
            return
        x, y = pyautogui.position()
        self.captured_coords = (x, y)
        self._close()
        if self.on_coords_captured:
            self.on_coords_captured(x, y)

    def _cancel(self) -> None:
        """Cancel picking"""
        if self._window is None:
            return
        self.captured_coords = None
        self._close()

    def _close(self) -> None:
        """Clean up"""
        if self._polling_id and self._window:
            self._window.after_cancel(self._polling_id)
            self._polling_id = None
        if self._window:
            try:
                self._window.grab_release()
            except tk.TclError:
                pass
            try:
                self._window.destroy()
            except tk.TclError:
                pass
            self._window = None

    def is_active(self) -> bool:
        return self._window is not None
