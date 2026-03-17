"""Workflow data models"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class StepType(str, Enum):
    """Enumeration of all supported step types"""
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    TYPE_TEXT = "type_text"
    WAIT = "wait"
    INSERT_COLUMN_VALUE = "insert_column_value"
    PRESS_HOTKEY = "press_hotkey"
    COPY_FIELD = "copy_field"


class ExecutionStatus(str, Enum):
    """Enumeration of execution session status"""
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    COMPLETED = "completed"


class Hotkey(str, Enum):
    """Enumeration of supported hotkeys"""
    ESCAPE = "Escape"
    ENTER = "Enter"
    BACKSPACE = "Backspace"
    TAB = "Tab"
    SHIFT_TAB = "Shift+Tab"
    CTRL_A = "Ctrl+A"
    CTRL_C = "Ctrl+C"
    CTRL_V = "Ctrl+V"


@dataclass
class WorkflowStep:
    """A single action in a workflow"""
    type: StepType
    order: int
    params: Dict
    
    def validate(self, available_columns: Optional[List[str]] = None) -> List[str]:
        """Validate step parameters and return list of errors"""
        errors = []
        
        if self.type == StepType.CLICK:
            if "x" not in self.params or not isinstance(self.params["x"], int):
                errors.append("Click step requires 'x' parameter (integer)")
            if "y" not in self.params or not isinstance(self.params["y"], int):
                errors.append("Click step requires 'y' parameter (integer)")

        elif self.type == StepType.DOUBLE_CLICK:
            if "x" not in self.params or not isinstance(self.params["x"], int):
                errors.append("Double-click step requires 'x' parameter (integer)")
            if "y" not in self.params or not isinstance(self.params["y"], int):
                errors.append("Double-click step requires 'y' parameter (integer)")
                
        elif self.type == StepType.TYPE_TEXT:
            if "text" not in self.params or not isinstance(self.params["text"], str) or not self.params["text"]:
                errors.append("Type-text step requires 'text' parameter (non-empty string)")
                
        elif self.type == StepType.WAIT:
            if "duration_ms" not in self.params:
                errors.append("Wait step requires 'duration_ms' parameter")
            else:
                duration = self.params["duration_ms"]
                if not isinstance(duration, int) or duration < 50:
                    errors.append("Wait step requires 'duration_ms' parameter (integer >= 50)")
                    
        elif self.type == StepType.INSERT_COLUMN_VALUE:
            if "column_name" not in self.params or not isinstance(self.params["column_name"], str):
                errors.append("Insert-column-value step requires 'column_name' parameter")
            elif available_columns and self.params["column_name"] not in available_columns:
                errors.append(f"Column '{self.params['column_name']}' not found in available columns")
                
        elif self.type == StepType.PRESS_HOTKEY:
            if "hotkey" not in self.params or not isinstance(self.params["hotkey"], str) or not self.params["hotkey"]:
                errors.append("Press-hotkey step requires 'hotkey' parameter (non-empty string)")
        
        return errors


@dataclass
class Workflow:
    """Represents a saved, reusable automation sequence"""
    name: str
    steps: List[WorkflowStep] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamps if not provided"""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def validate(self, available_columns: Optional[List[str]] = None) -> List[str]:
        """Validate all steps in the workflow"""
        errors = []
        
        for step in self.steps:
            step_errors = step.validate(available_columns)
            errors.extend([f"Step {step.order} ({step.type}): {err}" for err in step_errors])
        
        return errors
    
    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow"""
        self.steps.append(step)
        self._reorder_steps()
        self.updated_at = datetime.utcnow()
    
    def remove_step(self, step_order: int) -> None:
        """Remove a step by its order index"""
        self.steps = [s for s in self.steps if s.order != step_order]
        self._reorder_steps()
        self.updated_at = datetime.utcnow()
    
    def move_step(self, from_order: int, to_order: int) -> None:
        """Move a step from one position to another"""
        if from_order == to_order:
            return
        
        # Find the step
        step_to_move = None
        for step in self.steps:
            if step.order == from_order:
                step_to_move = step
                break
        
        if step_to_move is None:
            return
        
        # Remove from old position
        self.steps.remove(step_to_move)
        
        # Insert at new position
        # Adjust orders
        for step in self.steps:
            if step.order >= to_order:
                step.order += 1
        
        step_to_move.order = to_order
        self.steps.append(step_to_move)
        
        self._reorder_steps()
        self.updated_at = datetime.utcnow()
    
    def _reorder_steps(self) -> None:
        """Reorder steps to ensure sequential order indices"""
        sorted_steps = sorted(self.steps, key=lambda s: s.order)
        for i, step in enumerate(sorted_steps):
            step.order = i
        self.steps = sorted_steps


@dataclass
class ExcelDataSource:
    """Represents the imported Excel workbook and selected worksheet"""
    file_path: str
    sheet_name: str
    headers: List[str] = field(default_factory=list)
    row_count: int = 0
    
    def validate(self) -> List[str]:
        """Validate the data source"""
        errors = []
        
        if not self.file_path.endswith('.xlsx'):
            errors.append("Excel file must be a .xlsx file")
        
        if self.row_count > 10000:
            errors.append("Maximum 10,000 rows allowed")
        
        return errors


@dataclass
class LogEntry:
    """A single logged action within an execution session"""
    timestamp: datetime
    row: int
    step_type: str
    detail: str
    dry_run: bool = False
    
    def to_dict(self) -> Dict:
        """Convert log entry to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "row": self.row,
            "step_type": self.step_type,
            "detail": self.detail,
            "dry_run": self.dry_run
        }


@dataclass
class ExecutionSession:
    """Represents a single run of a workflow against a data source"""
    workflow: Workflow
    data_source: ExcelDataSource
    start_row: int = 1
    current_row: int = 0
    status: ExecutionStatus = ExecutionStatus.IDLE
    dry_run: bool = False
    log_entries: List[LogEntry] = field(default_factory=list)
    
    def can_start(self) -> bool:
        """Check if execution can be started"""
        return self.status == ExecutionStatus.IDLE and self.start_row >= 1
    
    def can_stop(self) -> bool:
        """Check if execution can be stopped"""
        return self.status == ExecutionStatus.RUNNING
    
    def start(self) -> None:
        """Start the execution session"""
        if not self.can_start():
            raise ValueError(f"Cannot start execution in status: {self.status}")
        self.status = ExecutionStatus.RUNNING
        self.current_row = self.start_row
    
    def stop(self) -> None:
        """Stop the execution session"""
        if not self.can_stop():
            raise ValueError(f"Cannot stop execution in status: {self.status}")
        self.status = ExecutionStatus.STOPPED
    
    def complete(self) -> None:
        """Mark the execution session as completed"""
        if self.status != ExecutionStatus.RUNNING:
            raise ValueError(f"Cannot complete execution in status: {self.status}")
        self.status = ExecutionStatus.COMPLETED
    
    def reset(self) -> None:
        """Reset the session to idle state"""
        self.status = ExecutionStatus.IDLE
        self.current_row = 0
    
    def add_log_entry(self, entry: LogEntry) -> None:
        """Add a log entry to the session"""
        self.log_entries.append(entry)
