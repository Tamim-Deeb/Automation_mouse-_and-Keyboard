"""Step editor forms for configuring workflow steps"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict
from src.workflow.models import StepType, Hotkey


class StepEditorDialog:
    """
    Dialog for creating/editing a workflow step.
    Shows appropriate form fields based on step type.
    """
    
    def __init__(self, parent: tk.Tk, step_type: StepType, on_save: Callable, on_pick_coords: Optional[Callable] = None):
        """
        Initialize the step editor dialog.
        
        Args:
            parent: Parent window
            step_type: Type of step to edit
            on_save: Callback when step is saved (receives params dict)
            on_pick_coords: Callback for coordinate picker (receives callback for coords)
        """
        self.parent = parent
        self.step_type = step_type
        self.on_save = on_save
        self.on_pick_coords = on_pick_coords
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit {step_type.value.replace('_', ' ').title()} Step")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.params: Dict = {}
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create form widgets based on step type"""
        # Main container
        container = ttk.Frame(self.dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Step type label
        ttk.Label(
            container,
            text=f"Step Type: {self.step_type.value.replace('_', ' ').title()}",
            font=('TkDefaultFont', 10, 'bold')
        ).pack(pady=(0, 20))
        
        # Create appropriate form fields
        if self.step_type in [StepType.CLICK, StepType.DOUBLE_CLICK]:
            self._create_coordinate_fields(container)
        elif self.step_type == StepType.TYPE_TEXT:
            self._create_text_field(container)
        elif self.step_type == StepType.WAIT:
            self._create_wait_field(container)
        elif self.step_type == StepType.INSERT_COLUMN_VALUE:
            self._create_column_field(container)
        elif self.step_type == StepType.PRESS_HOTKEY:
            self._create_hotkey_field(container)
        
        # Button frame
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=self._on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _create_coordinate_fields(self, container: ttk.Frame) -> None:
        """Create X and Y coordinate fields"""
        # X coordinate
        x_frame = ttk.Frame(container)
        x_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(x_frame, text="X:").pack(side=tk.LEFT)
        self.x_entry = ttk.Entry(x_frame, width=15)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        
        # Pick button
        if self.on_pick_coords:
            ttk.Button(
                x_frame,
                text="Pick",
                command=lambda: self.on_pick_coords(self._on_coords_picked)
            ).pack(side=tk.LEFT, padx=5)
        
        # Y coordinate
        y_frame = ttk.Frame(container)
        y_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(y_frame, text="Y:").pack(side=tk.LEFT)
        self.y_entry = ttk.Entry(y_frame, width=15)
        self.y_entry.pack(side=tk.LEFT, padx=5)
    
    def _on_coords_picked(self, x: int, y: int) -> None:
        """Handle coordinate picker callback"""
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))
    
    def _create_text_field(self, container: ttk.Frame) -> None:
        """Create text field for type_text step"""
        ttk.Label(container, text="Text to type:").pack(anchor=tk.W, pady=(5, 0))
        
        self.text_entry = ttk.Entry(container, width=40)
        self.text_entry.pack(fill=tk.X, pady=5)
    
    def _create_wait_field(self, container: ttk.Frame) -> None:
        """Create duration field for wait step"""
        ttk.Label(container, text="Duration (milliseconds):").pack(anchor=tk.W, pady=(5, 0))
        ttk.Label(container, text="(minimum: 50ms)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)
        
        self.duration_entry = ttk.Entry(container, width=15)
        self.duration_entry.pack(pady=5)
        self.duration_entry.insert(0, "500")
    
    def _create_column_field(self, container: ttk.Frame) -> None:
        """Create column dropdown for insert_column_value step"""
        ttk.Label(container, text="Column:").pack(anchor=tk.W, pady=(5, 0))
        
        self.column_var = tk.StringVar()
        self.column_dropdown = ttk.OptionMenu(container, self.column_var, "", *[])
        self.column_dropdown.pack(fill=tk.X, pady=5)
    
    def _create_hotkey_field(self, container: ttk.Frame) -> None:
        """Create hotkey dropdown for press_hotkey step"""
        ttk.Label(container, text="Hotkey:").pack(anchor=tk.W, pady=(5, 0))
        
        hotkeys = [h.value for h in Hotkey]
        self.hotkey_var = tk.StringVar()
        self.hotkey_dropdown = ttk.OptionMenu(container, self.hotkey_var, hotkeys[0], *hotkeys)
        self.hotkey_dropdown.pack(fill=tk.X, pady=5)
    
    def _on_save(self) -> None:
        """Handle save button click"""
        # Validate and collect parameters based on step type
        if self.step_type in [StepType.CLICK, StepType.DOUBLE_CLICK]:
            try:
                x = int(self.x_entry.get())
                y = int(self.y_entry.get())
                self.params = {"x": x, "y": y}
            except ValueError as e:
                tk.messagebox.showerror("Validation Error", str(e))
                return
        
        elif self.step_type == StepType.TYPE_TEXT:
            text = self.text_entry.get().strip()
            if not text:
                tk.messagebox.showerror("Validation Error", "Text cannot be empty")
                return
            self.params = {"text": text}
        
        elif self.step_type == StepType.WAIT:
            try:
                duration = int(self.duration_entry.get())
                if duration < 50:
                    tk.messagebox.showerror("Validation Error", "Duration must be at least 50ms")
                    return
                self.params = {"duration_ms": duration}
            except ValueError:
                tk.messagebox.showerror("Validation Error", "Duration must be a number")
                return
        
        elif self.step_type == StepType.INSERT_COLUMN_VALUE:
            column = self.column_var.get()
            if not column:
                tk.messagebox.showerror("Validation Error", "Please select a column")
                return
            self.params = {"column_name": column}
        
        elif self.step_type == StepType.PRESS_HOTKEY:
            self.params = {"hotkey": self.hotkey_var.get()}
        
        # Call save callback
        self.on_save(self.params)
        self.dialog.destroy()
    
    def set_columns(self, columns: list[str]) -> None:
        """
        Set available columns for insert_column_value step.
        
        Args:
            columns: List of column names
        """
        if self.step_type == StepType.INSERT_COLUMN_VALUE:
            menu = self.column_dropdown["menu"]
            menu.delete(0, tk.END)
            
            for column in columns:
                menu.add_command(
                    label=column,
                    command=lambda c=column: self.column_var.set(c)
                )


class AddStepDialog:
    """
    Dialog for selecting a step type to add.
    """
    
    def __init__(self, parent: tk.Tk, on_step_type_selected: Callable[[StepType], None]):
        """
        Initialize the add step dialog.
        
        Args:
            parent: Parent window
            on_step_type_selected: Callback when step type is selected
        """
        self.parent = parent
        self.on_step_type_selected = on_step_type_selected
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Step")
        self.dialog.geometry("300x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create step type selection widgets"""
        # Main container
        container = ttk.Frame(self.dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            container,
            text="Select Step Type:",
            font=('TkDefaultFont', 10, 'bold')
        ).pack(pady=(0, 15))
        
        # Step type buttons
        step_types = [
            (StepType.CLICK, "Click"),
            (StepType.DOUBLE_CLICK, "Double Click"),
            (StepType.TYPE_TEXT, "Type Text"),
            (StepType.WAIT, "Wait"),
            (StepType.INSERT_COLUMN_VALUE, "Insert Column Value"),
            (StepType.PRESS_HOTKEY, "Press Hotkey"),
        ]
        
        for step_type, label in step_types:
            btn = ttk.Button(
                container,
                text=label,
                width=30,
                command=lambda st=step_type: self._on_step_selected(st)
            )
            btn.pack(pady=5)
        
        # Cancel button
        ttk.Button(
            container,
            text="Cancel",
            width=30,
            command=self.dialog.destroy
        ).pack(pady=(20, 0))
    
    def _on_step_selected(self, step_type: StepType) -> None:
        """Handle step type selection"""
        self.dialog.destroy()
        self.on_step_type_selected(step_type)
