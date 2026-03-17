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
