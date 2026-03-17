"""Keyboard automation via pyautogui"""
import time
import pyautogui
import warnings
from src.workflow.models import Hotkey


class KeyboardAutomation:
    """
    Keyboard automation wrapper.
    Supports character-by-character typing and hotkey combinations.
    Supports character-by-character typing and hotkey combinations.
    """
    
    # Default delay between keystrokes (milliseconds)
    DEFAULT_INTER_KEY_DELAY_MS = 50
    
    SUPPORTED_HOTKEYS = {
        Hotkey.ESCAPE: ['escape'],
        Hotkey.ENTER: ['enter'],
        Hotkey.BACKSPACE: ['backspace'],
        Hotkey.TAB: ['tab'],
        Hotkey.SHIFT_TAB: ['shift', 'tab'],
        Hotkey.CTRL_A: ['ctrl', 'a'],
        Hotkey.CTRL_C: ['ctrl', 'c'],
        Hotkey.CTRL_V: ['ctrl', 'v'],
    }
    
    def __init__(self, inter_key_delay_ms: int = DEFAULT_INTER_KEY_DELAY_MS):
        """
        Initialize keyboard automation.
        
        Args:
            inter_key_delay_ms: Delay in milliseconds between keystrokes
        """
        self.inter_key_delay_ms = max(0, inter_key_delay_ms)
    
    def type_text(self, text: str) -> bool:
        """
        Type text character-by-character.
        
        Args:
            text: The text to type
            
        Returns:
            True if typing was successful, False otherwise
        """
        if not text:
            warnings.warn("Empty text provided for typing. Skipping.")
            return False
        
        try:
            # pyautogui.write types character by character
            pyautogui.write(text, interval=self.inter_key_delay_ms / 1000.0)
            return True
        except Exception as e:
            warnings.warn(f"Failed to type text: {e}")
            return False
    
    def press_hotkey(self, hotkey: Hotkey) -> bool:
        """
        Press a hotkey combination.
        
        Args:
            hotkey: The hotkey to press (from Hotkey enum)
            
        Returns:
            True if hotkey was pressed successfully, False otherwise
        """
        if hotkey not in self.SUPPORTED_HOTKEYS:
            warnings.warn(f"Unsupported hotkey: {hotkey}. Supported hotkeys: {list(self.SUPPORTED_HOTKEYS.keys())}")
            return False
        
        try:
            keys = self.SUPPORTED_HOTKEYS[hotkey]
            pyautogui.hotkey(*keys)
            self._apply_delay()
            return True
        except Exception as e:
            warnings.warn(f"Failed to press hotkey {hotkey}: {e}")
            return False
    
    def press_hotkey_by_string(self, hotkey_str: str) -> bool:
        """
        Press a hotkey by its string representation.
        
        Args:
            hotkey_str: String representation of the hotkey (e.g., "Enter", "Ctrl+A")
            
        Returns:
            True if hotkey was pressed successfully, False otherwise
        """
        try:
            hotkey = Hotkey(hotkey_str)
            return self.press_hotkey(hotkey)
        except ValueError:
            warnings.warn(f"Invalid hotkey string: {hotkey_str}")
            return False
    
    def _apply_delay(self) -> None:
        """Apply the configured delay after an operation"""
        if self.inter_key_delay_ms > 0:
            time.sleep(self.inter_key_delay_ms / 1000.0)
    
    def set_inter_key_delay(self, delay_ms: int) -> None:
        """
        Set the delay between keystrokes.
        
        Args:
            delay_ms: Delay in milliseconds
        """
        self.inter_key_delay_ms = max(0, delay_ms)
    
    @staticmethod
    def get_supported_hotkeys() -> list[Hotkey]:
        """
        Get the list of supported hotkeys.
        
        Returns:
            List of supported Hotkey enum values
        """
        return list(KeyboardAutomation.SUPPORTED_HOTKEYS.keys())
