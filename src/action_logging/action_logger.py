"""Action logger for workflow execution"""
import os
from datetime import datetime
from typing import Optional
from src.workflow.models import LogEntry


class ActionLogger:
    """
    Logs workflow execution actions to a file with timestamps.
    Supports dry-run mode with [DRY-RUN] prefix.
    Writes incrementally to handle large log volumes.
    """
    
    def __init__(self, log_file_path: Optional[str] = None):
        """
        Initialize the action logger.
        
        Args:
            log_file_path: Path to the log file. If None, generates a timestamped filename.
        """
        if log_file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file_path = f"workflow_log_{timestamp}.txt"
        
        self.log_file_path = log_file_path
        self._file_handle = None
        self._entry_count = 0
    
    def start(self) -> None:
        """Start logging by opening the log file"""
        try:
            # Create directory if it doesn't exist
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Open file in append mode with UTF-8 encoding
            self._file_handle = open(self.log_file_path, 'a', encoding='utf-8')
            
            # Write session header
            self._write_line("=" * 60)
            self._write_line(f"Workflow Execution Log - {datetime.now().isoformat()}")
            self._write_line("=" * 60)
            self._write_line("")
            
        except IOError as e:
            raise IOError(f"Failed to open log file {self.log_file_path}: {e}")
    
    def log(self, entry: LogEntry) -> None:
        """
        Log an action entry to the file.
        
        Args:
            entry: The LogEntry to log
        """
        if self._file_handle is None:
            raise RuntimeError("Logger not started. Call start() first.")
        
        # Format the log entry
        dry_run_prefix = "[DRY-RUN] " if entry.dry_run else ""
        timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        log_line = f"{timestamp_str} | Row {entry.row} | {entry.step_type} | {dry_run_prefix}{entry.detail}"
        
        self._write_line(log_line)
        self._entry_count += 1
    
    def log_message(self, message: str, dry_run: bool = False) -> None:
        """
        Log a generic message.
        
        Args:
            message: The message to log
            dry_run: Whether this is a dry-run message
        """
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            row=0,
            step_type="MESSAGE",
            detail=message,
            dry_run=dry_run
        )
        self.log(entry)
    
    def _write_line(self, line: str) -> None:
        """
        Write a line to the log file and flush.
        
        Args:
            line: The line to write
        """
        if self._file_handle:
            self._file_handle.write(line + "\n")
            self._file_handle.flush()
    
    def stop(self) -> None:
        """Stop logging by closing the log file"""
        if self._file_handle is not None:
            try:
                self._write_line("")
                self._write_line(f"Session completed. Total entries: {self._entry_count}")
                self._write_line("=" * 60)
                self._file_handle.close()
            except IOError:
                pass
            finally:
                self._file_handle = None
    
    def get_entry_count(self) -> int:
        """
        Get the number of log entries written.
        
        Returns:
            Number of entries logged
        """
        return self._entry_count
    
    def get_log_file_path(self) -> str:
        """
        Get the path to the log file.
        
        Returns:
            Path to the log file
        """
        return self.log_file_path
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
        return False
