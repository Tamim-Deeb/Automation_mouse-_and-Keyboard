"""Step type registry for extensible step handler registration"""
from typing import Callable, Dict, Optional
from src.workflow.models import WorkflowStep, StepType, ExecutionSession


# Type alias for step handler functions
StepHandler = Callable[
    [WorkflowStep, ExecutionSession, Dict[str, str]],
    None
]


class StepRegistry:
    """
    Registry for step handlers that enables adding new step types
    without modifying existing code (Constitution III).
    """
    
    def __init__(self):
        """Initialize an empty registry"""
        self._handlers: Dict[StepType, StepHandler] = {}
    
    def register(self, step_type: StepType, handler: StepHandler) -> None:
        """
        Register a handler function for a step type.
        
        Args:
            step_type: The step type to register
            handler: Function that executes the step. Signature:
                handler(step: WorkflowStep, session: ExecutionSession, row_data: Dict[str, str]) -> None
        """
        self._handlers[step_type] = handler
    
    def get_handler(self, step_type: StepType) -> Optional[StepHandler]:
        """
        Get the handler for a step type.
        
        Args:
            step_type: The step type to look up
            
        Returns:
            The handler function, or None if not registered
        """
        return self._handlers.get(step_type)
    
    def has_handler(self, step_type: StepType) -> bool:
        """
        Check if a handler is registered for a step type.
        
        Args:
            step_type: The step type to check
            
        Returns:
            True if a handler is registered, False otherwise
        """
        return step_type in self._handlers
    
    def unregister(self, step_type: StepType) -> None:
        """
        Unregister a handler for a step type.
        
        Args:
            step_type: The step type to unregister
        """
        if step_type in self._handlers:
            del self._handlers[step_type]
    
    def list_registered_types(self) -> list[StepType]:
        """
        Get a list of all registered step types.
        
        Returns:
            List of registered step types
        """
        return list(self._handlers.keys())


# Global registry instance
_global_registry = StepRegistry()


def register_step_handler(step_type: StepType, handler: StepHandler) -> None:
    """
    Register a step handler with the global registry.
    
    Args:
        step_type: The step type to register
        handler: The handler function
    """
    _global_registry.register(step_type, handler)


def get_step_handler(step_type: StepType) -> Optional[StepHandler]:
    """
    Get a step handler from the global registry.
    
    Args:
        step_type: The step type to look up
        
    Returns:
        The handler function, or None if not registered
    """
    return _global_registry.get_handler(step_type)


def get_global_registry() -> StepRegistry:
    """
    Get the global step registry instance.
    
    Returns:
        The global StepRegistry instance
    """
    return _global_registry
