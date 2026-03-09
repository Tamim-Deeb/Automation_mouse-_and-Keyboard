"""Integration tests for coordinate picker"""
import tkinter as tk
import pytest
from src.gui.coordinate_picker import CoordinatePicker


@pytest.fixture
def root_window():
    """Create a root window for testing"""
    root = tk.Tk()
    root.withdraw()  # Hide the window
    yield root
    root.destroy()


def test_coordinate_picker_creation(root_window):
    """Test that coordinate picker can be created"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    
    assert picker is not None
    assert not picker.is_active()


def test_coordinate_picker_pick_starts_overlay(root_window):
    """Test that pick() starts the overlay"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    picker.pick()
    
    # Overlay should be active
    assert picker.is_active()
    
    # Clean up
    picker._close()


def test_coordinate_picker_callback(root_window):
    """Test that callback is called with coordinates"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    
    # Simulate a click event
    picker._on_click(type('Event', (), {'x': 100, 'y': 200}))
    
    # Check that callback was called
    assert len(captured_coords) == 1
    assert captured_coords[0] == (100, 200)


def test_coordinate_picker_cancel(root_window):
    """Test that Esc key cancels the picker"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    picker.pick()
    
    # Simulate Esc key press
    picker._on_cancel(None)
    
    # Overlay should be closed
    assert not picker.is_active()
    
    # No coordinates should have been captured
    assert len(captured_coords) == 0


def test_coordinate_picker_multiple_clicks(root_window):
    """Test that multiple clicks work correctly"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    
    # Simulate multiple clicks
    picker._on_click(type('Event', (), {'x': 100, 'y': 200}))
    
    # Create new picker for second click
    picker2 = CoordinatePicker(root_window, on_coords_captured)
    picker2._on_click(type('Event', (), {'x': 300, 'y': 400}))
    
    # Check that both clicks were captured
    assert len(captured_coords) == 2
    assert captured_coords[0] == (100, 200)
    assert captured_coords[1] == (300, 400)


def test_coordinate_picker_is_active(root_window):
    """Test is_active() method"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    
    # Initially not active
    assert not picker.is_active()
    
    # After pick(), should be active
    picker.pick()
    assert picker.is_active()
    
    # After close(), should not be active
    picker._close()
    assert not picker.is_active()


def test_coordinate_picker_context_manager(root_window):
    """Test using coordinate picker as context manager"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    with CoordinatePicker(root_window, on_coords_captured) as picker:
        # Should be active inside context
        assert picker.is_active()
    
    # Should be closed after exiting context
    assert not picker.is_active()


def test_coordinate_picker_valid_coordinates(root_window):
    """Test that valid coordinates are captured correctly"""
    captured_coords = []
    
    def on_coords_captured(x, y):
        captured_coords.append((x, y))
    
    picker = CoordinatePicker(root_window, on_coords_captured)
    
    # Test various valid coordinates
    test_coords = [
        (0, 0),
        (100, 200),
        (1920, 1080),
        (500, 500),
    ]
    
    for x, y in test_coords:
        picker._on_click(type('Event', (), {'x': x, 'y': y}))
    
    assert len(captured_coords) == len(test_coords)
    assert captured_coords == test_coords
