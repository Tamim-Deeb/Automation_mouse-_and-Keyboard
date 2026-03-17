"""Mouse automation via pyautogui"""
import time
import pyautogui
import warnings


class MouseAutomation:
    """
    Mouse automation wrapper with screen bounds validation.
    Supports single click and double click at specified coordinates.
    """
    
    # Default delay between operations (milliseconds)
    DEFAULT_DELAY_MS = 100
    
    def __init__(self, delay_ms: int = DEFAULT_DELAY_MS):
        """
        Initialize mouse automation.
        
        Args:
            delay_ms: Delay in milliseconds after each operation
        """
        self.delay_ms = delay_ms
        self.screen_width, self.screen_height = pyautogui.size()
    
    def click(self, x: int, y: int) -> bool:
        """
        Perform a single mouse click at the specified coordinates.
        
        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            
        Returns:
            True if click was executed, False if coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y):
            warnings.warn(f"Coordinates ({x}, {y}) are out of screen bounds. Skipping click.")
            return False
        
        try:
            pyautogui.click(x, y)
            self._apply_delay()
            return True
        except Exception as e:
            warnings.warn(f"Failed to click at ({x}, {y}): {e}")
            return False
    
    def double_click(self, x: int, y: int) -> bool:
        """
        Perform a double mouse click at the specified coordinates.
        
        Args:
            x: X coordinate (pixels)
            y: Y coordinate (pixels)
            
        Returns:
            True if double-click was executed, False if coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y):
            warnings.warn(f"Coordinates ({x}, {y}) are out of screen bounds. Skipping double-click.")
            return False
        
        try:
            pyautogui.doubleClick(x, y)
            self._apply_delay()
            return True
        except Exception as e:
            warnings.warn(f"Failed to double-click at ({x}, {y}): {e}")
            return False
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """
        Perform a mouse drag from start to end coordinates.

        Presses the left mouse button at (start_x, start_y), moves to
        (end_x, end_y), then releases the button.

        Args:
            start_x: X coordinate of drag start
            start_y: Y coordinate of drag start
            end_x: X coordinate of drag end
            end_y: Y coordinate of drag end

        Returns:
            True if drag was executed, False on failure
        """
        if not self._validate_coordinates(start_x, start_y):
            warnings.warn(f"Start coordinates ({start_x}, {start_y}) are out of screen bounds. Skipping drag.")
            return False
        if not self._validate_coordinates(end_x, end_y):
            warnings.warn(f"End coordinates ({end_x}, {end_y}) are out of screen bounds. Skipping drag.")
            return False

        try:
            pyautogui.mouseDown(start_x, start_y)
            pyautogui.moveTo(end_x, end_y, duration=0.5)
            pyautogui.mouseUp()
            self._apply_delay()
            return True
        except Exception as e:
            warnings.warn(f"Failed to drag from ({start_x}, {start_y}) to ({end_x}, {end_y}): {e}")
            return False

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """
        Validate that coordinates are within screen bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if coordinates are valid, False otherwise
        """
        return True
    
    def _apply_delay(self) -> None:
        """Apply the configured delay after an operation"""
        if self.delay_ms > 0:
            time.sleep(self.delay_ms / 1000.0)
    
    def get_screen_size(self) -> tuple[int, int]:
        """
        Get the current screen size.
        
        Returns:
            Tuple of (width, height) in pixels
        """
        return self.screen_width, self.screen_height
    
    def set_delay(self, delay_ms: int) -> None:
        """
        Set the delay between operations.
        
        Args:
            delay_ms: Delay in milliseconds
        """
        self.delay_ms = max(0, delay_ms)
