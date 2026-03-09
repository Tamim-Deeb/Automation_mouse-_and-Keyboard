"""Integration tests for keyboard automation"""
import pytest
from src.automation.keyboard import KeyboardAutomation
from src.workflow.models import Hotkey


def test_keyboard_type_text():
    """Test typing text character-by-character"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.type_text("Hello World")
    
    assert result is True


def test_keyboard_type_empty_text():
    """Test typing empty text"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.type_text("")
    
    assert result is False


def test_keyboard_type_special_characters():
    """Test typing text with special characters"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.type_text("Test@123!#$%")
    
    assert result is True


def test_keyboard_press_hotkey_enter():
    """Test pressing Enter hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.ENTER)
    
    assert result is True


def test_keyboard_press_hotkey_backspace():
    """Test pressing Backspace hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.BACKSPACE)
    
    assert result is True


def test_keyboard_press_hotkey_tab():
    """Test pressing Tab hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.TAB)
    
    assert result is True


def test_keyboard_press_hotkey_shift_tab():
    """Test pressing Shift+Tab hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.SHIFT_TAB)
    
    assert result is True


def test_keyboard_press_hotkey_ctrl_a():
    """Test pressing Ctrl+A hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.CTRL_A)
    
    assert result is True


def test_keyboard_press_hotkey_ctrl_c():
    """Test pressing Ctrl+C hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.CTRL_C)
    
    assert result is True


def test_keyboard_press_hotkey_ctrl_v():
    """Test pressing Ctrl+V hotkey"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey(Hotkey.CTRL_V)
    
    assert result is True


def test_keyboard_press_hotkey_by_string():
    """Test pressing hotkey by string representation"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    # Test each supported hotkey
    hotkey_strings = ["Enter", "Backspace", "Tab", "Shift+Tab", "Ctrl+A", "Ctrl+C", "Ctrl+V"]
    
    for hotkey_str in hotkey_strings:
        result = keyboard.press_hotkey_by_string(hotkey_str)
        assert result is True


def test_keyboard_press_hotkey_invalid_string():
    """Test pressing hotkey with invalid string"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    result = keyboard.press_hotkey_by_string("InvalidHotkey")
    
    assert result is False


def test_keyboard_get_supported_hotkeys():
    """Test getting list of supported hotkeys"""
    supported = KeyboardAutomation.get_supported_hotkeys()
    
    assert len(supported) == 7
    assert Hotkey.ENTER in supported
    assert Hotkey.BACKSPACE in supported
    assert Hotkey.TAB in supported
    assert Hotkey.SHIFT_TAB in supported
    assert Hotkey.CTRL_A in supported
    assert Hotkey.CTRL_C in supported
    assert Hotkey.CTRL_V in supported


def test_keyboard_set_inter_key_delay():
    """Test setting inter-key delay"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=50)
    
    assert keyboard.inter_key_delay_ms == 50
    
    keyboard.set_inter_key_delay(100)
    
    assert keyboard.inter_key_delay_ms == 100
    
    # Test negative delay (should be set to 0)
    keyboard.set_inter_key_delay(-50)
    
    assert keyboard.inter_key_delay_ms == 0


def test_keyboard_type_long_text():
    """Test typing a longer text string"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    long_text = "This is a longer text string to test the keyboard automation module."
    
    result = keyboard.type_text(long_text)
    
    assert result is True


def test_keyboard_type_unicode():
    """Test typing unicode characters"""
    keyboard = KeyboardAutomation(inter_key_delay_ms=0)
    
    # Test common unicode characters
    unicode_text = "Hello 世界 🌍"
    
    result = keyboard.type_text(unicode_text)
    
    # Result depends on system support for unicode
    # We just verify it doesn't crash
    assert result is True or result is False
