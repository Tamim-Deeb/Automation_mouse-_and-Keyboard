"""Main application entry point - wires all panels together"""
import sys
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from typing import Optional
import pyautogui
from src.workflow.models import Workflow, ExecutionSession, ExcelDataSource
from src.gui.app import App
from src.gui.excel_panel import ExcelPanel
from src.gui.workflow_panel import WorkflowPanel
from src.gui.execution_panel import ExecutionPanel
from src.workflow.serializer import WorkflowSerializer


def is_frozen() -> bool:
    """
    Check if the application is running as a frozen PyInstaller bundle.
    
    Returns:
        True if running as a frozen executable, False otherwise
    """
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to a resource, handling both frozen and normal execution.
    
    When running as a frozen PyInstaller bundle, resources are extracted to
    sys._MEIPASS. In normal execution, paths are relative to the script.
    
    Args:
        relative_path: Path relative to the resource root (e.g., 'assets/app.ico')
    
    Returns:
        Absolute path to the resource
    """
    if is_frozen():
        # Running in PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        # Get the directory containing this script
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get to the project root
        base_path = os.path.dirname(base_path)
    
    return os.path.join(base_path, relative_path)


class MainApp:
    """
    Main application that wires all panels together.
    Coordinates Excel import, workflow building, and execution.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.workflow: Workflow = Workflow(name="Workflow", steps=[])
        self.data_source: Optional[ExcelDataSource] = None
        self.session: Optional[ExecutionSession] = None
        self.serializer = WorkflowSerializer()
        
        self._create_ui()
        self._register_step_handlers()
    
    def _create_ui(self) -> None:
        """Create the user interface"""
        # Create main app shell
        self.app = App(self.root)
        
        # Replace placeholder panels with actual implementations
        self._setup_excel_panel()
        self._setup_workflow_panel()
        self._setup_execution_panel()
        self._setup_menu_handlers()
    
    def _setup_excel_panel(self) -> None:
        """Setup Excel panel with callback"""
        # Clear placeholder content
        for widget in self.app.excel_panel.winfo_children():
            widget.destroy()
        
        # Create actual Excel panel
        self.excel_panel = ExcelPanel(
            self.app.excel_panel,
            on_data_loaded=self._on_excel_data_loaded
        )
    
    def _setup_workflow_panel(self) -> None:
        """Setup workflow panel with callback"""
        # Clear placeholder content
        for widget in self.app.workflow_panel.winfo_children():
            widget.destroy()
        
        # Create actual workflow panel
        self.workflow_panel = WorkflowPanel(
            self.app.workflow_panel,
            on_step_added=self._on_step_added
        )
    
    def _setup_execution_panel(self) -> None:
        """Setup execution panel with callback"""
        # Clear placeholder content
        for widget in self.app.execution_panel.winfo_children():
            widget.destroy()
        
        # Create actual execution panel
        self.execution_panel = ExecutionPanel(
            self.app.execution_panel,
            on_execution_complete=self._on_execution_complete
        )
    
    def _setup_menu_handlers(self) -> None:
        """Setup menu bar handlers"""
        # We need to replace the menu handlers in the app
        menubar = self.root.nametowidget(self.root.cget("menu"))
        
        # Get File menu
        file_menu = menubar.winfo_children()[0]
        
        # Replace handlers by reconfiguring menu items
        # This is a workaround since tkinter doesn't allow easy menu item replacement
        # We'll create new menu items
        
        # Clear and recreate File menu
        file_menu.delete(0, tk.END)
        file_menu.add_command(label="New Workflow", command=self._on_new_workflow)
        file_menu.add_command(label="Open Workflow...", command=self._on_open_workflow)
        file_menu.add_command(label="Save Workflow", command=self._on_save_workflow)
        file_menu.add_command(label="Save Workflow As...", command=self._on_save_workflow_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_exit)
    
    def _register_step_handlers(self) -> None:
        """Register step handlers with the step registry"""
        from src.engine.step_registry import register_step_handler
        from src.workflow.models import StepType
        from src.automation.mouse import MouseAutomation
        from src.automation.keyboard import KeyboardAutomation
        from src.automation.wait import WaitModule
        from src.automation.clipboard import ClipboardModule
        from src.excel.writer import ExcelWriter
        
        # Create automation instances
        self.mouse = MouseAutomation(delay_ms=0)
        self.keyboard = KeyboardAutomation(inter_key_delay_ms=0)
        self.wait = WaitModule()
        self.clipboard = ClipboardModule()
        self.excel_writer = ExcelWriter()
        
        # Register handlers
        def click_handler(step, session, row_data):
            x = step.params["x"]
            y = step.params["y"]
            self.mouse.click(x, y)
        
        def double_click_handler(step, session, row_data):
            x = step.params["x"]
            y = step.params["y"]
            self.mouse.double_click(x, y)
        
        def type_text_handler(step, session, row_data):
            text = step.params["text"]
            self.keyboard.type_text(text)
        
        def wait_handler(step, session, row_data):
            duration_ms = step.params["duration_ms"]
            self.wait.sleep(duration_ms)
        
        def insert_column_value_handler(step, session, row_data):
            column_name = step.params["column_name"]
            value = row_data.get(column_name, "")
            self.keyboard.type_text(value)
        
        def press_hotkey_handler(step, session, row_data):
            hotkey_str = step.params["hotkey"]
            self.keyboard.press_hotkey_by_string(hotkey_str)
        
        def copy_field_handler(step, session, row_data):
            # Clear clipboard
            self.clipboard.clear()
            time.sleep(0.05)  # 50ms delay
            # Select all
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.05)  # 50ms delay
            # Copy
            pyautogui.hotkey('ctrl', 'c')
        
        def click_and_move_handler(step, session, row_data):
            self.mouse.drag(
                step.params["start_x"], step.params["start_y"],
                step.params["end_x"], step.params["end_y"]
            )

        def write_to_excel_handler(step, session, row_data):
            write_mode = step.params["write_mode"]
            column_name = step.params["column_name"]
            if write_mode == "mark_done":
                value = "x"
            else:
                value = self.clipboard.paste()
            excel_row = session.current_row + 1  # header is row 1, data starts row 2
            self.excel_writer.write_cell(
                session.data_source.file_path,
                session.data_source.sheet_name,
                excel_row,
                column_name,
                value
            )

        def screen_loaded_handler(step, session, row_data):
            """Handler for screen_loaded step - waits for text to appear on screen"""
            start_x = step.params["start_x"]
            start_y = step.params["start_y"]
            end_x = step.params["end_x"]
            end_y = step.params["end_y"]
            max_tries = step.params["max_tries"]

            screen_loaded = False
            for attempt in range(max_tries):
                # Check if session has been stopped (e.g., by kill-switch)
                if session.status != "running":
                    return

                # Clear clipboard
                self.clipboard.clear()
                time.sleep(0.05)  # 50ms delay

                # Drag to select text
                self.mouse.drag(start_x, start_y, end_x, end_y)
                time.sleep(0.05)  # 50ms delay

                # Copy selected text
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.05)  # 50ms delay

                # Check if clipboard has content
                clipboard_content = self.clipboard.paste().strip()
                if clipboard_content:
                    screen_loaded = True
                    break

                # Wait before retry (1 second, interruptible by kill-switch)
                if attempt < max_tries - 1:
                    kill_switch = self.execution_panel.kill_switch
                    if kill_switch:
                        was_interrupted = self.wait.interruptible_sleep(1000, kill_switch.event)
                        if was_interrupted:
                            session.stop()
                            return
                    else:
                        self.wait.sleep(1000)

            # If max tries exceeded without success, stop the workflow
            if not screen_loaded and session.status == "running":
                session.stop()

        register_step_handler(StepType.CLICK, click_handler)
        register_step_handler(StepType.DOUBLE_CLICK, double_click_handler)
        register_step_handler(StepType.TYPE_TEXT, type_text_handler)
        register_step_handler(StepType.WAIT, wait_handler)
        register_step_handler(StepType.INSERT_COLUMN_VALUE, insert_column_value_handler)
        register_step_handler(StepType.PRESS_HOTKEY, press_hotkey_handler)
        register_step_handler(StepType.COPY_FIELD, copy_field_handler)
        register_step_handler(StepType.CLICK_AND_MOVE, click_and_move_handler)
        register_step_handler(StepType.WRITE_TO_EXCEL, write_to_excel_handler)
        register_step_handler(StepType.SCREEN_LOADED, screen_loaded_handler)
    
    # Excel panel callback
    def _on_excel_data_loaded(self, headers: list[str], row_count: int) -> None:
        """Handle Excel data loaded"""
        self.data_source = ExcelDataSource(
            file_path=self.excel_panel.file_path,
            sheet_name=self.excel_panel.selected_sheet,
            headers=headers,
            row_count=row_count
        )
        
        # Update workflow panel with available columns
        self.workflow_panel.set_available_columns(headers)
        
        # Update execution session
        self._update_session()
    
    # Workflow panel callback
    def _on_step_added(self, step) -> None:
        """Handle step added to workflow"""
        self.workflow = self.workflow_panel.get_workflow()
        self._update_session()
    
    # Execution panel callback
    def _on_execution_complete(self, status_message: str) -> None:
        """Handle execution completion"""
        # Reset session
        if self.session:
            self.session.reset()
    
    # Menu handlers
    def _on_new_workflow(self) -> None:
        """Handle New Workflow menu command"""
        result = messagebox.askyesno(
            "New Workflow",
            "Create a new workflow? Any unsaved changes will be lost."
        )
        
        if result:
            self.workflow = Workflow(name="Workflow", steps=[])
            self.workflow_panel.clear()
            self.data_source = None
            self.session = None
    
    def _on_open_workflow(self) -> None:
        """Handle Open Workflow menu command"""
        file_path = filedialog.askopenfilename(
            title="Open Workflow",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            workflow = self.serializer.load(file_path)
            self.workflow = workflow
            self.workflow_panel.set_workflow(workflow)
            self._update_session()
            messagebox.showinfo("Success", f"Workflow loaded from:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load workflow:\n{e}")
    
    def _on_save_workflow(self) -> None:
        """Handle Save Workflow menu command"""
        if not hasattr(self, '_current_save_path') or not self._current_save_path:
            self._on_save_workflow_as()
        else:
            self._save_to_file(self._current_save_path)
    
    def _on_save_workflow_as(self) -> None:
        """Handle Save Workflow As menu command"""
        file_path = filedialog.asksaveasfilename(
            title="Save Workflow As",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path: str) -> None:
        """Save workflow to file"""
        try:
            self.workflow = self.workflow_panel.get_workflow()
            self.serializer.save(self.workflow, file_path)
            self._current_save_path = file_path
            messagebox.showinfo("Success", f"Workflow saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workflow:\n{e}")
    
    def _on_exit(self) -> None:
        """Handle Exit menu command"""
        result = messagebox.askyesno(
            "Exit",
            "Exit the application? Any unsaved changes will be lost."
        )
        
        if result:
            self.root.quit()
    
    def _update_session(self) -> None:
        """Update execution session with current workflow and data source"""
        if self.data_source and self.workflow.steps:
            self.session = ExecutionSession(
                workflow=self.workflow,
                data_source=self.data_source,
                start_row=1,
                current_row=0,
                status="idle",
                dry_run=False,
                log_entries=[]
            )
            self.execution_panel.set_session(self.session)
        else:
            self.session = None
            self.execution_panel.set_session(None)


def main():
    """Entry point for the application"""
    try:
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()
    except Exception as e:
        # Handle any startup errors
        show_startup_error(e)
        raise


def show_startup_error(error: Exception) -> None:
    """
    Display a user-friendly error dialog when the app fails to start.
    
    This is especially important when running as a frozen executable
    with no console window, as errors would otherwise be silent.
    
    Args:
        error: The exception that occurred during startup
    """
    try:
        # Create a hidden root window for the messagebox
        error_root = tk.Tk()
        error_root.withdraw()  # Hide the main window
        
        # Build user-friendly error message
        error_type = type(error).__name__
        error_msg = str(error)
        
        # Create detailed message
        message = f"Failed to start the application.\n\n"
        message += f"Error: {error_type}\n"
        message += f"Details: {error_msg}\n\n"
        message += "Please ensure you have the required permissions and try again."
        
        # Show error dialog
        messagebox.showerror(
            title="Startup Error",
            message=message,
            parent=error_root
        )
        
        # Clean up
        error_root.destroy()
    except Exception:
        # If we can't even show the error dialog, at least print to stderr
        import traceback
        print("CRITICAL: Failed to start application and show error dialog", file=sys.stderr)
        traceback.print_exc()


if __name__ == "__main__":
    main()
