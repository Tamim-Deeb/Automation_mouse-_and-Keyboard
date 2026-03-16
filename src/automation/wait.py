"""Wait/timing module with minimum delay enforcement"""
import time
import threading


class WaitModule:
    """
    Wait module for timed delays in workflows.
    Enforces minimum 50ms delay per constitution timing guard.
    """
    
    # Minimum delay in milliseconds (constitution requirement)
    MIN_DELAY_MS = 50
    
    def __init__(self):
        """Initialize the wait module"""
        pass
    
    def sleep(self, duration_ms: int) -> None:
        """
        Sleep for the specified duration.
        Enforces minimum 50ms delay per constitution.
        
        Args:
            duration_ms: Duration in milliseconds (will be enforced to minimum 50ms)
        """
        # Enforce minimum delay
        actual_duration_ms = max(duration_ms, self.MIN_DELAY_MS)
        
        # Convert to seconds and sleep
        time.sleep(actual_duration_ms / 1000.0)
    
    def interruptible_sleep(self, duration_ms: int, stop_event: threading.Event) -> bool:
        """
        Sleep for the specified duration, but can be interrupted by the stop event.
        Enforces minimum 50ms delay per constitution.
        
        Args:
            duration_ms: Duration in milliseconds (will be enforced to minimum 50ms)
            stop_event: Threading event that can interrupt the sleep
            
        Returns:
            True if sleep was interrupted by stop_event, False otherwise
        """
        # Enforce minimum delay
        actual_duration_ms = max(duration_ms, self.MIN_DELAY_MS)
        
        # Convert to seconds
        timeout_seconds = actual_duration_ms / 1000.0
        
        # Wait for the stop event or timeout
        was_interrupted = stop_event.wait(timeout=timeout_seconds)
        
        return was_interrupted
    
    @staticmethod
    def get_min_delay() -> int:
        """
        Get the minimum allowed delay.
        
        Returns:
            Minimum delay in milliseconds
        """
        return WaitModule.MIN_DELAY_MS
    
    @staticmethod
    def validate_duration(duration_ms: int) -> bool:
        """
        Validate that a duration meets the minimum requirement.
        
        Args:
            duration_ms: Duration in milliseconds
            
        Returns:
            True if duration is valid, False otherwise
        """
        return duration_ms >= WaitModule.MIN_DELAY_MS
