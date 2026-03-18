"""Step editor forms for configuring workflow steps"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict
from src.workflow.models import StepType, Hotkey
from src.gui.theme import center_dialog


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
        if step_type == StepType.CLICK_AND_MOVE:
            dialog_height = 450
        elif step_type == StepType.WRITE_TO_EXCEL:
            dialog_height = 350
        elif step_type == StepType.SCREEN_LOADED:
            dialog_height = 500
        elif step_type == StepType.CONDITION:
            dialog_height = 350
        else:
            dialog_height = 300
        self.dialog.geometry(f"400x{dialog_height}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.params: Dict = {}
        
        self._create_widgets()
        center_dialog(self.dialog)
    
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
        elif self.step_type == StepType.CLICK_AND_MOVE:
            self._create_drag_coordinate_fields(container)
        elif self.step_type == StepType.WRITE_TO_EXCEL:
            self._create_write_to_excel_fields(container)
        elif self.step_type == StepType.SCREEN_LOADED:
            self._create_screen_loaded_fields(container)
        elif self.step_type == StepType.CONDITION:
            self._create_condition_fields(container)

        # Button frame
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=self._on_save, style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy, style="Custom.TButton").pack(side=tk.LEFT, padx=5)
    
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
                command=lambda: self.on_pick_coords(self._on_coords_picked),
                style="Custom.TButton"
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
        
        # Re-center and focus dialog after coordinate picking
        self.dialog.deiconify()
        self.dialog.lift()
        self.dialog.focus_force()
        center_dialog(self.dialog)
    
    def _create_drag_coordinate_fields(self, container: ttk.Frame) -> None:
        """Create start and end coordinate fields for click_and_move step"""
        # Start position
        ttk.Label(container, text="Start Position:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(5, 0))

        start_x_frame = ttk.Frame(container)
        start_x_frame.pack(fill=tk.X, pady=2)
        ttk.Label(start_x_frame, text="X:").pack(side=tk.LEFT)
        self.start_x_entry = ttk.Entry(start_x_frame, width=15)
        self.start_x_entry.pack(side=tk.LEFT, padx=5)
        if self.on_pick_coords:
            ttk.Button(
                start_x_frame, text="Pick",
                command=lambda: self.on_pick_coords(self._on_start_coords_picked),
                style="Custom.TButton"
            ).pack(side=tk.LEFT, padx=5)

        start_y_frame = ttk.Frame(container)
        start_y_frame.pack(fill=tk.X, pady=2)
        ttk.Label(start_y_frame, text="Y:").pack(side=tk.LEFT)
        self.start_y_entry = ttk.Entry(start_y_frame, width=15)
        self.start_y_entry.pack(side=tk.LEFT, padx=5)

        # End position
        ttk.Label(container, text="End Position:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(10, 0))

        end_x_frame = ttk.Frame(container)
        end_x_frame.pack(fill=tk.X, pady=2)
        ttk.Label(end_x_frame, text="X:").pack(side=tk.LEFT)
        self.end_x_entry = ttk.Entry(end_x_frame, width=15)
        self.end_x_entry.pack(side=tk.LEFT, padx=5)
        if self.on_pick_coords:
            ttk.Button(
                end_x_frame, text="Pick",
                command=lambda: self.on_pick_coords(self._on_end_coords_picked),
                style="Custom.TButton"
            ).pack(side=tk.LEFT, padx=5)

        end_y_frame = ttk.Frame(container)
        end_y_frame.pack(fill=tk.X, pady=2)
        ttk.Label(end_y_frame, text="Y:").pack(side=tk.LEFT)
        self.end_y_entry = ttk.Entry(end_y_frame, width=15)
        self.end_y_entry.pack(side=tk.LEFT, padx=5)

    def _on_start_coords_picked(self, x: int, y: int) -> None:
        """Handle coordinate picker callback for start position"""
        self.start_x_entry.delete(0, tk.END)
        self.start_x_entry.insert(0, str(x))
        self.start_y_entry.delete(0, tk.END)
        self.start_y_entry.insert(0, str(y))
        
        # Re-center and focus dialog after coordinate picking
        self.dialog.deiconify()
        self.dialog.lift()
        self.dialog.focus_force()
        center_dialog(self.dialog)

    def _on_end_coords_picked(self, x: int, y: int) -> None:
        """Handle coordinate picker callback for end position"""
        self.end_x_entry.delete(0, tk.END)
        self.end_x_entry.insert(0, str(x))
        self.end_y_entry.delete(0, tk.END)
        self.end_y_entry.insert(0, str(y))
        
        # Re-center and focus dialog after coordinate picking
        self.dialog.deiconify()
        self.dialog.lift()
        self.dialog.focus_force()
        center_dialog(self.dialog)

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
        """Create hotkey dropdown and custom input fields for press_hotkey step"""
        ttk.Label(container, text="Hotkey:").pack(anchor=tk.W, pady=(5, 0))

        hotkeys = [h.value for h in Hotkey]
        self.hotkey_var = tk.StringVar()
        self.hotkey_dropdown = ttk.OptionMenu(container, self.hotkey_var, hotkeys[0], *hotkeys)
        self.hotkey_dropdown.pack(fill=tk.X, pady=5)

        # Custom hotkey input
        ttk.Label(container, text="— OR enter custom hotkey —", font=('TkDefaultFont', 8)).pack(pady=(10, 5))

        ttk.Label(container, text="Modifier (optional):").pack(anchor=tk.W)
        self.modifier_entry = ttk.Entry(container, width=30)
        self.modifier_entry.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(container, text="Key:").pack(anchor=tk.W)
        self.key_entry = ttk.Entry(container, width=30)
        self.key_entry.pack(fill=tk.X, pady=(0, 5))
    
    def _create_write_to_excel_fields(self, container: ttk.Frame) -> None:
        """Create column dropdown and write mode selector for write_to_excel step"""
        # Column dropdown
        ttk.Label(container, text="Target Column:").pack(anchor=tk.W, pady=(5, 0))

        self.write_column_var = tk.StringVar()
        self.write_column_dropdown = ttk.OptionMenu(container, self.write_column_var, "", *[])
        self.write_column_dropdown.pack(fill=tk.X, pady=5)

        # Write mode selector
        ttk.Label(container, text="Write Mode:").pack(anchor=tk.W, pady=(10, 0))

        self.write_mode_var = tk.StringVar(value="mark_done")

        mode_frame = ttk.Frame(container)
        mode_frame.pack(fill=tk.X, pady=5)

        ttk.Radiobutton(
            mode_frame, text="Mark Done (x)", variable=self.write_mode_var, value="mark_done"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            mode_frame, text="Paste Clipboard", variable=self.write_mode_var, value="paste_clipboard"
        ).pack(anchor=tk.W)

    def _create_screen_loaded_fields(self, container: ttk.Frame) -> None:
        """Create start and end coordinate fields and max tries for screen_loaded step"""
        # Start position
        ttk.Label(container, text="Start Position:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(5, 0))

        start_x_frame = ttk.Frame(container)
        start_x_frame.pack(fill=tk.X, pady=2)
        ttk.Label(start_x_frame, text="X:").pack(side=tk.LEFT)
        self.screen_start_x_entry = ttk.Entry(start_x_frame, width=15)
        self.screen_start_x_entry.pack(side=tk.LEFT, padx=5)
        if self.on_pick_coords:
            ttk.Button(
                start_x_frame, text="Pick",
                command=lambda: self.on_pick_coords(self._on_screen_start_coords_picked),
                style="Custom.TButton"
            ).pack(side=tk.LEFT, padx=5)

        start_y_frame = ttk.Frame(container)
        start_y_frame.pack(fill=tk.X, pady=2)
        ttk.Label(start_y_frame, text="Y:").pack(side=tk.LEFT)
        self.screen_start_y_entry = ttk.Entry(start_y_frame, width=15)
        self.screen_start_y_entry.pack(side=tk.LEFT, padx=5)

        # End position
        ttk.Label(container, text="End Position:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(10, 0))

        end_x_frame = ttk.Frame(container)
        end_x_frame.pack(fill=tk.X, pady=2)
        ttk.Label(end_x_frame, text="X:").pack(side=tk.LEFT)
        self.screen_end_x_entry = ttk.Entry(end_x_frame, width=15)
        self.screen_end_x_entry.pack(side=tk.LEFT, padx=5)
        if self.on_pick_coords:
            ttk.Button(
                end_x_frame, text="Pick",
                command=lambda: self.on_pick_coords(self._on_screen_end_coords_picked),
                style="Custom.TButton"
            ).pack(side=tk.LEFT, padx=5)

        end_y_frame = ttk.Frame(container)
        end_y_frame.pack(fill=tk.X, pady=2)
        ttk.Label(end_y_frame, text="Y:").pack(side=tk.LEFT)
        self.screen_end_y_entry = ttk.Entry(end_y_frame, width=15)
        self.screen_end_y_entry.pack(side=tk.LEFT, padx=5)

        # Max tries
        ttk.Label(container, text="Max Tries:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(container, text="(minimum: 1)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)

        max_tries_frame = ttk.Frame(container)
        max_tries_frame.pack(fill=tk.X, pady=2)
        self.max_tries_entry = ttk.Entry(max_tries_frame, width=15)
        self.max_tries_entry.pack(side=tk.LEFT)
        self.max_tries_entry.insert(0, "10")

    def _on_screen_start_coords_picked(self, x: int, y: int) -> None:
        """Handle coordinate picker callback for screen loaded start position"""
        self.screen_start_x_entry.delete(0, tk.END)
        self.screen_start_x_entry.insert(0, str(x))
        self.screen_start_y_entry.delete(0, tk.END)
        self.screen_start_y_entry.insert(0, str(y))
        
        # Re-center and focus dialog after coordinate picking
        self.dialog.deiconify()
        self.dialog.lift()
        self.dialog.focus_force()
        center_dialog(self.dialog)

    def _on_screen_end_coords_picked(self, x: int, y: int) -> None:
        """Handle coordinate picker callback for screen loaded end position"""
        self.screen_end_x_entry.delete(0, tk.END)
        self.screen_end_x_entry.insert(0, str(x))
        self.screen_end_y_entry.delete(0, tk.END)
        self.screen_end_y_entry.insert(0, str(y))
        
        # Re-center and focus dialog after coordinate picking
        self.dialog.deiconify()
        self.dialog.lift()
        self.dialog.focus_force()
        center_dialog(self.dialog)

    def _create_condition_fields(self, container: ttk.Frame) -> None:
        """Create fields for condition step: Equal checkbox, compare word, step count"""
        # Equal checkbox
        self.is_equal_var = tk.BooleanVar(value=True)
        equal_frame = ttk.Frame(container)
        equal_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(
            equal_frame, text="Equal", variable=self.is_equal_var
        ).pack(side=tk.LEFT)

        # Compare word
        ttk.Label(container, text="Compare Word:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(container, text="(leave empty to compare against empty clipboard)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)
        self.compare_word_entry = ttk.Entry(container, width=40)
        self.compare_word_entry.pack(fill=tk.X, pady=5)

        # Step count
        ttk.Label(container, text="Number of steps to govern:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(container, text="(minimum: 1)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)
        self.step_count_entry = ttk.Entry(container, width=15)
        self.step_count_entry.pack(pady=5)
        self.step_count_entry.insert(0, "1")

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
        
        elif self.step_type == StepType.CLICK_AND_MOVE:
            try:
                start_x = int(self.start_x_entry.get())
                start_y = int(self.start_y_entry.get())
                end_x = int(self.end_x_entry.get())
                end_y = int(self.end_y_entry.get())
                self.params = {"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y}
            except ValueError:
                tk.messagebox.showerror("Validation Error", "All coordinate fields must be valid numbers")
                return

        elif self.step_type == StepType.PRESS_HOTKEY:
            custom_key = self.key_entry.get().strip()
            custom_modifier = self.modifier_entry.get().strip()
            if custom_key:
                # Custom input takes priority over dropdown
                if custom_modifier:
                    hotkey_str = custom_modifier.lower() + "+" + custom_key.lower()
                else:
                    hotkey_str = custom_key.lower()
                self.params = {"hotkey": hotkey_str}
            elif custom_modifier and not custom_key:
                tk.messagebox.showerror("Validation Error", "Key is required for custom hotkey")
                return
            else:
                # Use dropdown selection
                self.params = {"hotkey": self.hotkey_var.get()}

        elif self.step_type == StepType.WRITE_TO_EXCEL:
            column = self.write_column_var.get()
            if not column:
                tk.messagebox.showerror("Validation Error", "Please select a target column")
                return
            write_mode = self.write_mode_var.get()
            self.params = {"column_name": column, "write_mode": write_mode}

        elif self.step_type == StepType.SCREEN_LOADED:
            try:
                start_x = int(self.screen_start_x_entry.get())
                start_y = int(self.screen_start_y_entry.get())
                end_x = int(self.screen_end_x_entry.get())
                end_y = int(self.screen_end_y_entry.get())
                max_tries = int(self.max_tries_entry.get())
                if max_tries < 1:
                    tk.messagebox.showerror("Validation Error", "Max tries must be at least 1")
                    return
                self.params = {"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y, "max_tries": max_tries}
            except ValueError:
                tk.messagebox.showerror("Validation Error", "All coordinate fields and max tries must be valid numbers")
                return

        elif self.step_type == StepType.CONDITION:
            try:
                step_count = int(self.step_count_entry.get())
                if step_count < 1:
                    tk.messagebox.showerror("Validation Error", "Step count must be at least 1")
                    return
                self.params = {
                    "compare_word": self.compare_word_entry.get(),
                    "is_equal": self.is_equal_var.get(),
                    "step_count": step_count
                }
            except ValueError:
                tk.messagebox.showerror("Validation Error", "Step count must be a valid number")
                return

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
        elif self.step_type == StepType.WRITE_TO_EXCEL:
            menu = self.write_column_dropdown["menu"]
            menu.delete(0, tk.END)

            for column in columns:
                menu.add_command(
                    label=column,
                    command=lambda c=column: self.write_column_var.set(c)
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
        self.dialog.geometry("320x580")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        center_dialog(self.dialog)
    
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
            (StepType.COPY_FIELD, "Copy Field"),
            (StepType.CLICK_AND_MOVE, "Click And Move"),
            (StepType.WRITE_TO_EXCEL, "Write To Excel"),
            (StepType.SCREEN_LOADED, "Screen Loaded"),
            (StepType.CONDITION, "Condition"),
        ]
        
        for step_type, label in step_types:
            btn = ttk.Button(
                container,
                text=label,
                width=30,
                command=lambda st=step_type: self._on_step_selected(st),
                style="Custom.TButton"
            )
            btn.pack(pady=5)
        
        # Cancel button
        ttk.Button(
            container,
            text="Cancel",
            width=30,
            command=self.dialog.destroy,
            style="Custom.TButton"
        ).pack(pady=(20, 0))
    
    def _on_step_selected(self, step_type: StepType) -> None:
        """Handle step type selection"""
        self.dialog.destroy()
        self.on_step_type_selected(step_type)
