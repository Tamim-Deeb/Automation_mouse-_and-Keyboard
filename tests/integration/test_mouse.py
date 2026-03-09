"""Integration tests for mouse automation"""
import pytest
from src.automation.mouse import MouseAutomation


def test_mouse_click_valid_coordinates():
    """Test mouse click with valid coordinates"""
    mouse = MouseAutomation(delay_ms=0)
    
    # Get screen size to find valid coordinates
    screen_width, screen_height = mouse.get_screen_size()
    
    # Test click at center of screen
    x = screen_width // 2
    y = screen_height // 2
    
    result = mouse.click(x, y)
    
    assert result is True


def test_mouse_click_out_of_bounds():
    """Test mouse click with out-of-bounds coordinates"""
    mouse = MouseAutomation(delay_ms=0)
    
    screen_width, screen_height = mouse.get_screen_size()
    
    # Test with coordinates outside screen bounds
    result = mouse.click(screen_width + 100, screen_height + 100)
    
    assert result is False


def test_mouse_click_negative_coordinates():
    """Test mouse click with negative coordinates"""
    mouse = MouseAutomation(delay_ms=0)
    
    result = mouse.click(-10, -10)
    
    assert result is False


def test_mouse_double_click_valid_coordinates():
    """Test mouse double-click with valid coordinates"""
    mouse = MouseAutomation(delay_ms=0)
    
    # Get screen size to find valid coordinates
    screen_width, screen_height = mouse.get_screen_size()
    
    # Test double-click at center of screen
    x = screen_width // 2
    y = screen_height // 2
    
    result = mouse.double_click(x, y)
    
    assert result is True


def test_mouse_double_click_out_of_bounds():
    """Test mouse double-click with out-of-bounds coordinates"""
    mouse = MouseAutomation(delay_ms=0)
    
    screen_width, screen_height = mouse.get_screen_size()
    
    # Test with coordinates outside screen bounds
    result = mouse.double_click(screen_width + 100, screen_height + 100)
    
    assert result is False


def test_mouse_get_screen_size():
    """Test getting screen size"""
    mouse = MouseAutomation(delay_ms=0)
    
    width, height = mouse.get_screen_size()
    
    assert isinstance(width, int)
    assert isinstance(height, int)
    assert width > 0
    assert height > 0


def test_mouse_set_delay():
    """Test setting delay between operations"""
    mouse = MouseAutomation(delay_ms=100)
    
    assert mouse.delay_ms == 100
    
    mouse.set_delay(200)
    
    assert mouse.delay_ms == 200
    
    # Test negative delay (should be set to 0)
    mouse.set_delay(-50)
    
    assert mouse.delay_ms == 0


def test_mouse_zero_coordinates():
    """Test mouse operations at (0, 0)"""
    mouse = MouseAutomation(delay_ms=0)
    
    # (0, 0) should be valid (top-left corner)
    result = mouse.click(0, 0)
    
    assert result is True
    
    result = mouse.double_click(0, 0)
    
    assert result is True


def test_mouse_edge_coordinates():
    """Test mouse operations at screen edges"""
    mouse = MouseAutomation(delay_ms=0)
    
    screen_width, screen_height = mouse.get_screen_size()
    
    # Test top edge
    result = mouse.click(screen_width // 2, 0)
    assert result is True
    
    # Test bottom edge (height - 1 is max valid coordinate)
    result = mouse.click(screen_width // 2, screen_height - 1)
    assert result is True
    
    # Test left edge
    result = mouse.click(0, screen_height // 2)
    assert result is True
    
    # Test right edge (width - 1 is max valid coordinate)
    result = mouse.click(screen_width - 1, screen_height // 2)
    assert result is True
