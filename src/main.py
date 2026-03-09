"""Main application entry point - wires all panels together"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from src.workflow.models import Workflow, ExecutionSession, ExcelDataSource
from src.gui.app import App
from src.gui.excel_panel import ExcelPanel
from src.gui.workflow_panel import WorkflowPanel
from src.gui.execution_panel import ExecutionPanel
from src.workflow.serializer import WorkflowSerializer


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
        
        # Create automation instances
        self.mouse = MouseAutomation(delay_ms=0)
        self.keyboard = KeyboardAutomation(inter_key_delay_ms=0)
        self.wait = WaitModule()
        
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
        
        register_step_handler(StepType.CLICK, click_handler)
        register_step_handler(StepType.DOUBLE_CLICK, double_click_handler)
        register_step_handler(StepType.TYPE_TEXT, type_text_handler)
        register_step_handler(StepType.WAIT, wait_handler)
        register_step_handler(StepType.INSERT_COLUMN_VALUE, insert_column_value_handler)
        register_step_handler(StepType.PRESS_HOTKEY, press_hotkey_handler)
    
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
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
