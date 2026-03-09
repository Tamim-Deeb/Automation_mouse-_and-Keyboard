"""Kill-switch listener for safe workflow termination"""
import threading
from pynput import keyboard
from typing import Optional


class KillSwitch:
    """
    Global keyboard listener for Esc key to stop workflow execution.
    Runs in a daemon thread and sets a threading.Event when triggered.
    """
    
    def __init__(self):
        """Initialize the kill-switch"""
        self._event = threading.Event()
        self._listener: Optional[keyboard.Listener] = None
        self._listener_thread: Optional[threading.Thread] = None
        self._is_running = False
    
    def start(self) -> None:
        """Start the kill-switch listener"""
        if self._is_running:
            return
        
        self._is_running = True
        self._event.clear()
        
        # Create keyboard listener
        def on_press(key):
            """Handle key press events"""
            try:
                # Check for Esc key
                if key == keyboard.Key.esc:
                    self._event.set()
            except AttributeError:
                pass
        
        # Create and start listener in a separate thread
        self._listener = keyboard.Listener(on_press=on_press)
        self._listener_thread = threading.Thread(target=self._listener.start, daemon=True)
        self._listener_thread.start()
    
    def stop(self) -> None:
        """Stop the kill-switch listener"""
        if not self._is_running:
            return
        
        self._is_running = False
        
        # Stop the listener
        if self._listener:
            self._listener.stop()
        
        # Wait for thread to finish
        if self._listener_thread:
            self._listener_thread.join(timeout=1.0)
    
    def trigger(self) -> None:
        """Manually trigger the kill-switch (for testing)"""
        self._event.set()
    
    def reset(self) -> None:
        """Reset the kill-switch event"""
        self._event.clear()
    
    def is_triggered(self) -> bool:
        """
        Check if the kill-switch has been triggered.
        
        Returns:
            True if triggered, False otherwise
        """
        return self._event.is_set()
    
    def is_running(self) -> bool:
        """
        Check if the kill-switch listener is running.
        
        Returns:
            True if running, False otherwise
        """
        return self._is_running
    
    def wait_for_trigger(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for the kill-switch to be triggered.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait indefinitely)
            
        Returns:
            True if triggered, False if timeout occurred
        """
        return self._event.wait(timeout=timeout)
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
        return False
