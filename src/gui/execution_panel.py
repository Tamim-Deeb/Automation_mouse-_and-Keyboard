"""Execution panel GUI for starting/stopping workflow execution"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import threading
from src.workflow.models import ExecutionSession, ExcelDataSource
from src.engine.executor import WorkflowExecutor
from src.engine.kill_switch import KillSwitch
from src.action_logging.action_logger import ActionLogger
from src.preferences import load_preferences, save_preferences


class ExecutionPanel:
    """
    Panel for starting, stopping, and monitoring workflow execution.
    Displays progress, start row, dry-run option, and status.
    """
    
    def __init__(
        self,
        parent: ttk.Frame,
        on_execution_complete: Optional[Callable[[str], None]] = None
    ):
        """
        Initialize execution panel.
        
        Args:
            parent: Parent widget
            on_execution_complete: Callback when execution completes
        """
        self.parent = parent
        self.on_execution_complete = on_execution_complete
        
        self.session: Optional[ExecutionSession] = None
        self.executor: Optional[WorkflowExecutor] = None
        self.kill_switch: Optional[KillSwitch] = None
        self.logger: Optional[ActionLogger] = None
        self.execution_thread: Optional[threading.Thread] = None
        
        # Register validation command
        self._validate_non_negative_int = (self.parent.register(self._is_non_negative_int), '%P')
        
        self._create_widgets()
    
    def _is_non_negative_int(self, value: str) -> bool:
        """
        Validate that the value is a non-negative integer.
        
        Args:
            value: The string value to validate
            
        Returns:
            True if valid, False otherwise
        """
        if value == "":
            return True  # Allow empty for now, will validate on start
        try:
            return int(value) >= 0
        except ValueError:
            return False
    
    def _create_widgets(self) -> None:
        """Create panel widgets"""
        # Start row input
        row_frame = ttk.Frame(self.parent)
        row_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row_frame, text="Start Row:").pack(side=tk.LEFT)
        self.start_row_var = tk.StringVar(value="1")
        self.start_row_entry = ttk.Entry(row_frame, textvariable=self.start_row_var, width=8)
        self.start_row_entry.pack(side=tk.LEFT, padx=5)
        
        # Dry-run checkbox
        self.dry_run_var = tk.BooleanVar(value=False)
        self.dry_run_chk = ttk.Checkbutton(
            self.parent,
            text="Dry Run",
            variable=self.dry_run_var
        )
        self.dry_run_chk.pack(side=tk.LEFT, padx=10)
        
        # Delay input
        delay_frame = ttk.Frame(self.parent)
        delay_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(delay_frame, text="Delay (ms):").pack(side=tk.LEFT)
        # Load saved delay or use default
        saved_prefs = load_preferences()
        default_delay = saved_prefs.get("step_delay_ms", 200)
        self.step_delay_var = tk.StringVar(value=str(default_delay))
        self.step_delay_entry = ttk.Entry(
            delay_frame,
            textvariable=self.step_delay_var,
            width=8,
            validate="key",
            validatecommand=self._validate_non_negative_int
        )
        self.step_delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Start button
        self.start_btn = ttk.Button(
            self.parent,
            text="Start",
            command=self._on_start,
            width=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = ttk.Button(
            self.parent,
            text="Stop",
            command=self._on_stop,
            width=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress label
        self.progress_label = ttk.Label(self.parent, text="Ready")
        self.progress_label.pack(side=tk.RIGHT, padx=10)
    
    def _on_start(self) -> None:
        """Handle Start button click"""
        if not self.session:
            messagebox.showwarning("No Workflow", "Please create a workflow first")
            return
        
        if not self.session.data_source:
            messagebox.showwarning("No Data", "Please import an Excel file first")
            return
        
        if not self.session.workflow.steps:
            messagebox.showwarning("No Steps", "Please add at least one step to the workflow")
            return
        
        # Check for zero-row worksheet
        if self.session.data_source.row_count == 0:
            messagebox.showwarning(
                "No Data Rows",
                "The selected worksheet has no data rows. Please select a worksheet with data."
            )
            return
        
        # Validate start row
        try:
            start_row = int(self.start_row_var.get())
            if start_row < 1 or start_row > self.session.data_source.row_count:
                messagebox.showerror(
                    "Invalid Start Row",
                    f"Start row must be between 1 and {self.session.data_source.row_count}"
                )
                return
        except ValueError:
            messagebox.showerror("Invalid Start Row", "Start row must be a number")
            return
        
        # Validate step delay
        try:
            delay_value = self.step_delay_var.get().strip()
            if delay_value == "":
                step_delay_ms = 200  # Default value
            else:
                step_delay_ms = int(delay_value)
                if step_delay_ms < 0:
                    messagebox.showerror(
                        "Invalid Delay",
                        "Delay must be a non-negative integer"
                    )
                    return
        except ValueError:
            messagebox.showerror("Invalid Delay", "Delay must be a number")
            return
        
        # Save delay value to preferences
        save_preferences({"step_delay_ms": step_delay_ms})
        
        # Update session
        self.session.start_row = start_row
        self.session.dry_run = self.dry_run_var.get()
        
        # Create logger
        self.logger = ActionLogger()
        
        # Create and start kill-switch
        self.kill_switch = KillSwitch()
        self.kill_switch.start()
        
        # Create executor with kill_switch and step_delay_ms
        self.executor = WorkflowExecutor(
            session=self.session,
            logger=self.logger,
            on_progress=self._on_progress,
            on_complete=self._on_complete,
            kill_switch=self.kill_switch,
            step_delay_ms=step_delay_ms
        )
        
        # Run executor in background thread
        self.execution_thread = threading.Thread(target=self.executor.execute, daemon=True)
        self.execution_thread.start()
        
        # Start kill-switch polling
        self._poll_kill_switch()
        
        # Update UI
        self._set_running_state(True)
    
    def _on_stop(self) -> None:
        """Handle Stop button click"""
        if self.executor:
            self.executor.stop()
        
        if self.kill_switch:
            self.kill_switch.trigger()
    
    def _on_progress(self, current_row: int, total_rows: int) -> None:
        """Handle progress update"""
        # Update progress label (must be thread-safe)
        self.parent.after(0, lambda: self.progress_label.config(
            text=f"Row {current_row} of {total_rows}"
        ))
    
    def _poll_kill_switch(self) -> None:
        """Poll the kill switch for Esc key presses"""
        if self.kill_switch and self.kill_switch.is_triggered():
            # Kill switch triggered - update progress label and stop execution
            self.progress_label.config(text="Stopping...")
            if self.executor:
                self.executor.stop()
            return
        
        # Schedule next poll (200ms)
        if self.executor and self.executor.is_running():
            self.parent.after(200, self._poll_kill_switch)
    
    def _on_complete(self, status_message: str) -> None:
        """Handle execution completion"""
        # Update UI (must be thread-safe)
        self.parent.after(0, lambda: self._update_complete(status_message))
    
    def _update_complete(self, status_message: str) -> None:
        """Update UI after completion"""
        # Check if stopped by Esc key
        was_stopped_by_esc = self.kill_switch and self.kill_switch.is_triggered()
        
        # Update progress label with appropriate message
        if was_stopped_by_esc:
            # Show "Stopped by Esc" message with row information
            if self.session:
                current_row = self.session.current_row
                total_rows = self.session.data_source.row_count if self.session.data_source else 0
                display_message = f"Stopped by Esc at row {current_row} of {total_rows}"
            else:
                display_message = "Stopped by Esc"
        else:
            display_message = status_message
        
        self.progress_label.config(text=display_message)
        self._set_running_state(False)
        
        # Stop kill-switch
        if self.kill_switch:
            self.kill_switch.stop()
            self.kill_switch = None
        
        # Notify callback
        if self.on_execution_complete:
            self.on_execution_complete(display_message)
        
        # Show log file location
        if self.logger:
            log_file = self.logger.get_log_file_path()
            messagebox.showinfo(
                "Execution Complete",
                f"{display_message}\n\nLog file: {log_file}"
            )
    
    def _set_running_state(self, running: bool) -> None:
        """Update UI state based on execution status"""
        if running:
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.start_row_entry.config(state=tk.DISABLED)
            self.dry_run_chk.config(state=tk.DISABLED)
            self.step_delay_entry.config(state=tk.DISABLED)
        else:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.start_row_entry.config(state=tk.NORMAL)
            self.dry_run_chk.config(state=tk.NORMAL)
            self.step_delay_entry.config(state=tk.NORMAL)
    
    def set_session(self, session: ExecutionSession) -> None:
        """
        Set the execution session.
        
        Args:
            session: Execution session to use
        """
        self.session = session
        
        # Update start row default
        if session and session.data_source:
            self.start_row_var.set(str(session.start_row))
    
    def is_running(self) -> bool:
        """
        Check if execution is currently running.
        
        Returns:
            True if running, False otherwise
        """
        return self.executor is not None and self.executor.is_running()
    
    def reset(self) -> None:
        """Reset the execution panel"""
        if self.executor and self.executor.is_running():
            self.executor.stop()
        
        if self.kill_switch:
            self.kill_switch.stop()
            self.kill_switch = None
        
        self.executor = None
        self.execution_thread = None
        self.logger = None
        
        self._set_running_state(False)
        self.progress_label.config(text="Ready")
