"""Integration tests for kill-switch"""
import time
import threading
import pytest
from src.engine.kill_switch import KillSwitch


def test_kill_switch_start_stop():
    """Test starting and stopping the kill-switch listener"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Verify it's running
    assert kill_switch.is_running()
    
    # Stop the listener
    kill_switch.stop()
    
    # Verify it's stopped
    assert not kill_switch.is_running()


def test_kill_switch_trigger():
    """Test triggering the kill-switch event"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Verify event is not set initially
    assert not kill_switch.is_triggered()
    
    # Trigger the kill-switch (simulating Esc key press)
    kill_switch.trigger()
    
    # Verify event is set
    assert kill_switch.is_triggered()
    
    # Stop the listener
    kill_switch.stop()
    
    # Reset for next test
    kill_switch.reset()


def test_kill_switch_reset():
    """Test resetting the kill-switch event"""
    kill_switch = KillSwitch()
    
    # Start and trigger
    kill_switch.start()
    kill_switch.trigger()
    
    # Verify it's triggered
    assert kill_switch.is_triggered()
    
    # Reset
    kill_switch.reset()
    
    # Verify it's no longer triggered
    assert not kill_switch.is_triggered()
    
    # Stop the listener
    kill_switch.stop()


def test_kill_switch_is_triggered():
    """Test checking if kill-switch is triggered"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Initially not triggered
    assert not kill_switch.is_triggered()
    
    # Trigger it
    kill_switch.trigger()
    
    # Now it should be triggered
    assert kill_switch.is_triggered()
    
    # Stop the listener
    kill_switch.stop()
    kill_switch.reset()


def test_kill_switch_is_running():
    """Test checking if kill-switch is running"""
    kill_switch = KillSwitch()
    
    # Initially not running
    assert not kill_switch.is_running()
    
    # Start it
    kill_switch.start()
    
    # Now it should be running
    assert kill_switch.is_running()
    
    # Stop it
    kill_switch.stop()
    
    # No longer running
    assert not kill_switch.is_running()


def test_kill_switch_response_time():
    """Test that kill-switch responds quickly (< 2 seconds)"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Record start time
    start_time = time.time()
    
    # Trigger the kill-switch in a separate thread
    def trigger_after_delay():
        time.sleep(0.1)  # Small delay
        kill_switch.trigger()
    
    trigger_thread = threading.Thread(target=trigger_after_delay)
    trigger_thread.start()
    
    # Wait for the event to be set
    kill_switch.wait_for_trigger(timeout=2.0)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Should be less than 2 seconds (constitution requirement)
    assert elapsed_time < 2.0
    
    # Stop the listener
    kill_switch.stop()
    kill_switch.reset()
    trigger_thread.join()


def test_kill_switch_wait_for_trigger():
    """Test waiting for kill-switch trigger"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Trigger after a short delay
    def trigger_after_delay():
        time.sleep(0.2)
        kill_switch.trigger()
    
    trigger_thread = threading.Thread(target=trigger_after_delay)
    trigger_thread.start()
    
    # Wait for trigger (should succeed)
    result = kill_switch.wait_for_trigger(timeout=1.0)
    
    assert result is True
    
    # Stop the listener
    kill_switch.stop()
    kill_switch.reset()
    trigger_thread.join()


def test_kill_switch_wait_timeout():
    """Test waiting for trigger with timeout"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Don't trigger, just wait for timeout
    result = kill_switch.wait_for_trigger(timeout=0.5)
    
    # Should timeout and return False
    assert result is False
    
    # Stop the listener
    kill_switch.stop()


def test_kill_switch_multiple_triggers():
    """Test that multiple triggers don't cause issues"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # Trigger multiple times
    kill_switch.trigger()
    kill_switch.trigger()
    kill_switch.trigger()
    
    # Should still be triggered
    assert kill_switch.is_triggered()
    
    # Stop the listener
    kill_switch.stop()
    kill_switch.reset()


def test_kill_switch_context_manager():
    """Test using kill-switch as context manager"""
    with KillSwitch() as kill_switch:
        # Should be running
        assert kill_switch.is_running()
        
        # Trigger it
        kill_switch.trigger()
        
        # Should be triggered
        assert kill_switch.is_triggered()
    
    # Should be stopped after exiting context
    assert not kill_switch.is_running()


def test_kill_switch_daemon_thread():
    """Test that kill-switch runs in a daemon thread"""
    kill_switch = KillSwitch()
    
    # Start the listener
    kill_switch.start()
    
    # The listener thread should be a daemon thread
    # (this prevents it from blocking program exit)
    assert kill_switch._listener_thread is not None
    assert kill_switch._listener_thread.daemon
    
    # Stop the listener
    kill_switch.stop()
