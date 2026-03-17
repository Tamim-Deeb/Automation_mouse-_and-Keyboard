"""Workflow execution engine"""
from typing import Optional, Callable, TYPE_CHECKING
from datetime import datetime
from src.workflow.models import Workflow, WorkflowStep, ExecutionSession, ExcelDataSource, LogEntry, StepType, Hotkey
from src.engine.step_registry import get_step_handler
from src.excel.reader import ExcelReader
from src.action_logging.action_logger import ActionLogger
from src.automation.wait import WaitModule

if TYPE_CHECKING:
    from src.engine.kill_switch import KillSwitch


class WorkflowExecutor:
    """
    Executes a workflow row-by-row against an Excel data source.
    Supports dry-run mode, kill-switch checking, and action logging.
    """
    
    def __init__(
        self,
        session: ExecutionSession,
        logger: Optional[ActionLogger] = None,
        on_progress: Optional[Callable[[int, int], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        kill_switch: Optional['KillSwitch'] = None,
        step_delay_ms: int = 0
    ):
        """
        Initialize the workflow executor.
        
        Args:
            session: Execution session containing workflow and data source
            logger: Optional action logger for recording actions
            on_progress: Callback for progress updates (current_row, total_rows)
            on_complete: Callback for completion (status message)
            kill_switch: Optional kill switch for safe stop functionality
            step_delay_ms: Optional delay in milliseconds to insert after each step (default: 0)
        """
        self.session = session
        self.logger = logger
        self.on_progress = on_progress
        self.on_complete = on_complete
        self.kill_switch = kill_switch
        self.step_delay_ms = step_delay_ms
        
        self._is_running = False
    
    def execute(self) -> None:
        """Execute the workflow"""
        if self._is_running:
            return
        
        self._is_running = True
        
        try:
            # Start logging
            if self.logger:
                self.logger.start()
            
            # Update session status
            self.session.start()
            
            # Load Excel data
            with ExcelReader(self.session.data_source.file_path) as reader:
                reader.load_workbook()
                reader.select_sheet(self.session.data_source.sheet_name)
                
                # Iterate over rows
                row_number = self.session.start_row
                total_rows = self.session.data_source.row_count
                
                for row_data in reader.iterate_rows(start_row=row_number):
                    # Check if stopped
                    if self.session.status != "running":
                        break
                    
                    # Check kill-switch between rows
                    if self.kill_switch and self.kill_switch.is_triggered():
                        self.session.stop()
                        break
                    
                    # Update current row
                    self.session.current_row = row_number
                    
                    # Execute each step for this row
                    for step in self.session.workflow.steps:
                        # Check kill-switch between steps
                        if self.kill_switch and self.kill_switch.is_triggered():
                            self.session.stop()
                            break
                        
                        # Check if stopped
                        if self.session.status != "running":
                            break
                        
                        self._execute_step(step, row_data, row_number)
                        
                        # Apply step delay after each step (if configured)
                        if self.step_delay_ms > 0:
                            wait = WaitModule()
                            if self.kill_switch:
                                # Use interruptible sleep with kill switch
                                was_interrupted = wait.interruptible_sleep(
                                    self.step_delay_ms,
                                    self.kill_switch.event
                                )
                                if was_interrupted:
                                    self.session.stop()
                                    break
                            else:
                                # No kill switch, use regular sleep
                                wait.sleep(self.step_delay_ms)
                    
                    # Check kill-switch after processing row
                    if self.kill_switch and self.kill_switch.is_triggered():
                        self.session.stop()
                        break
                    
                    # Notify progress
                    if self.on_progress:
                        self.on_progress(row_number, total_rows)
                    
                    row_number += 1
                
                # Update final status
                if self.session.status == "running":
                    self.session.complete()
                    if self.on_complete:
                        self.on_complete(f"Completed all {total_rows} rows")
                else:
                    if self.on_complete:
                        self.on_complete(f"Stopped at row {self.session.current_row} of {total_rows}")
        
        except Exception as e:
            # Log error
            if self.logger:
                self.logger.log_message(f"Error during execution: {e}", self.session.dry_run)
            
            # Update session status
            self.session.status = "stopped"
            
            if self.on_complete:
                self.on_complete(f"Error: {e}")
        
        finally:
            # Stop logging
            if self.logger:
                self.logger.stop()
            
            self._is_running = False
    
    def _execute_step(self, step: WorkflowStep, row_data: dict, row_number: int) -> None:
        """
        Execute a single workflow step.
        
        Args:
            step: The step to execute
            row_data: Dictionary of column values for the current row
            row_number: The current row number
        """
        # Get step handler
        handler = get_step_handler(step.type)
        
        if handler is None:
            error_msg = f"No handler registered for step type: {step.type}"
            self._log_error(step, row_number, error_msg)
            return
        
        # Log step start
        self._log_step_start(step, row_number)
        
        # Execute step (unless dry-run)
        if not self.session.dry_run:
            try:
                # Special handling for WAIT steps with kill switch
                if step.type == StepType.WAIT and self.kill_switch:
                    duration_ms = step.params.get("duration_ms", 0)
                    # Use kill switch wait_for_trigger for interruptible sleep
                    timeout_seconds = max(duration_ms, 50) / 1000.0  # Enforce 50ms minimum
                    was_triggered = self.kill_switch.wait_for_trigger(timeout=timeout_seconds)
                    if was_triggered:
                        self.session.stop()
                # Handle empty cells for insert_column_value
                elif step.type == StepType.INSERT_COLUMN_VALUE:
                    column_name = step.params.get("column_name", "")
                    value = row_data.get(column_name, "")
                    # Use empty string for blank cells
                    if value is None:
                        value = ""
                    # Update row_data with the value for the handler
                    row_data_with_value = row_data.copy()
                    row_data_with_value[column_name] = value
                    handler(step, self.session, row_data_with_value)
                # Suppress kill switch when automating Esc hotkey
                elif step.type == StepType.PRESS_HOTKEY and step.params.get("hotkey") == Hotkey.ESCAPE.value and self.kill_switch:
                    self.kill_switch.suppress()
                    try:
                        handler(step, self.session, row_data)
                    finally:
                        self.kill_switch.unsuppress()
                else:
                    handler(step, self.session, row_data)
            except Exception as e:
                self._log_error(step, row_number, str(e))
        else:
            # In dry-run mode, just log the action
            pass
        
        # Log step completion
        self._log_step_complete(step, row_number)
    
    def _log_step_start(self, step: WorkflowStep, row_number: int) -> None:
        """Log the start of a step execution"""
        detail = self._format_step_detail(step)
        
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            row=row_number,
            step_type=step.type.value,
            detail=f"Executing: {detail}",
            dry_run=self.session.dry_run
        )
        
        self.session.add_log_entry(entry)
        
        if self.logger:
            self.logger.log(entry)
    
    def _log_step_complete(self, step: WorkflowStep, row_number: int) -> None:
        """Log the completion of a step execution"""
        detail = self._format_step_detail(step)
        
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            row=row_number,
            step_type=step.type.value,
            detail=f"Completed: {detail}",
            dry_run=self.session.dry_run
        )
        
        self.session.add_log_entry(entry)
        
        if self.logger:
            self.logger.log(entry)
    
    def _log_error(self, step: WorkflowStep, row_number: int, error: str) -> None:
        """Log an error during step execution"""
        detail = self._format_step_detail(step)
        
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            row=row_number,
            step_type=step.type.value,
            detail=f"Error: {detail} - {error}",
            dry_run=self.session.dry_run
        )
        
        self.session.add_log_entry(entry)
        
        if self.logger:
            self.logger.log(entry)
    
    def _format_step_detail(self, step: WorkflowStep) -> str:
        """Format step details for logging"""
        if step.type == StepType.CLICK:
            return f"Click at ({step.params.get('x', 0)}, {step.params.get('y', 0)})"
        elif step.type == StepType.DOUBLE_CLICK:
            return f"Double-click at ({step.params.get('x', 0)}, {step.params.get('y', 0)})"
        elif step.type == StepType.TYPE_TEXT:
            text = step.params.get('text', '')
            if len(text) > 50:
                return f'Type text: "{text[:50]}..."'
            else:
                return f'Type text: "{text}"'
        elif step.type == StepType.WAIT:
            return f"Wait for {step.params.get('duration_ms', 0)}ms"
        elif step.type == StepType.INSERT_COLUMN_VALUE:
            column = step.params.get('column_name', '')
            return f"Insert column value: [{column}]"
        elif step.type == StepType.PRESS_HOTKEY:
            hotkey = step.params.get('hotkey', '')
            return f"Press hotkey: [{hotkey}]"
        elif step.type == StepType.WRITE_TO_EXCEL:
            column = step.params.get('column_name', '')
            mode = step.params.get('write_mode', '')
            return f"Write to Excel: [{column}] ({mode})"
        elif step.type == StepType.SCREEN_LOADED:
            return f"Screen loaded: ({step.params.get('start_x', '')}, {step.params.get('start_y', '')}) → ({step.params.get('end_x', '')}, {step.params.get('end_y', '')}) [max: {step.params.get('max_tries', '')}]"
        else:
            return step.type.value
    
    def stop(self) -> None:
        """Stop the execution"""
        if self.session.status == "running":
            self.session.stop()
    
    def is_running(self) -> bool:
        """
        Check if execution is running.
        
        Returns:
            True if running, False otherwise
        """
        return self._is_running
