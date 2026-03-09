"""Wait/timing module with minimum delay enforcement"""
import time


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
