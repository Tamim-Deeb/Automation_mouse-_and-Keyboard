"""Workflow panel GUI for building and managing workflow steps"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List
from src.workflow.models import Workflow, WorkflowStep, StepType
from src.gui.step_editors import AddStepDialog, StepEditorDialog


class WorkflowPanel:
    """
    Panel for building and managing workflow steps.
    Displays step list, add/reorder/delete functionality.
    """
    
    def __init__(self, parent: ttk.Frame, on_step_added: Optional[Callable] = None):
        """
        Initialize workflow panel.
        
        Args:
            parent: Parent widget
            on_step_added: Callback when a step is added
        """
        self.parent = parent
        self.on_step_added = on_step_added
        
        self.workflow: Optional[Workflow] = None
        self.steps: List[WorkflowStep] = []
        self.available_columns: List[str] = []
        self.selected_step_index: Optional[int] = None
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create panel widgets"""
        # Step list with scrollbar
        list_frame = ttk.Frame(self.parent)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.step_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=15
        )
        self.step_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.step_listbox.yview)
        
        # Bind selection change
        self.step_listbox.bind('<<ListboxSelect>>', self._on_selection_changed)
        
        # Button frame
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Add Step button
        ttk.Button(
            button_frame,
            text="Add Step",
            command=self._on_add_step,
            width=15
        ).pack(pady=5)
        
        ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Move Up button
        ttk.Button(
            button_frame,
            text="Move Up",
            command=self._on_move_up,
            width=15
        ).pack(pady=5)
        
        # Move Down button
        ttk.Button(
            button_frame,
            text="Move Down",
            command=self._on_move_down,
            width=15
        ).pack(pady=5)
        
        ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Delete Step button
        ttk.Button(
            button_frame,
            text="Delete Step",
            command=self._on_delete_step,
            width=15
        ).pack(pady=5)
        
        # Clear All button
        ttk.Button(
            button_frame,
            text="Clear All",
            command=self._on_clear_all,
            width=15
        ).pack(pady=5)
    
    def _on_selection_changed(self, event) -> None:
        """Handle step list selection change"""
        selection = self.step_listbox.curselection()
        if selection:
            self.selected_step_index = selection[0]
        else:
            self.selected_step_index = None
    
    def _on_add_step(self) -> None:
        """Handle Add Step button click"""
        def on_step_type_selected(step_type: StepType) -> None:
            """Handle step type selection"""
            # Create step editor dialog
            def on_save(params: dict) -> None:
                """Handle step save"""
                # Determine insertion position
                if self.selected_step_index is not None:
                    # Insert after selected step
                    insert_position = self.selected_step_index + 1
                else:
                    # Append to end
                    insert_position = len(self.steps)
                
                # Create new step
                new_step = WorkflowStep(
                    type=step_type,
                    order=insert_position,
                    params=params
                )
                
                # Insert at position
                self.steps.insert(insert_position, new_step)
                
                # Update orders
                self._reorder_steps()
                
                # Update display
                self._update_display()
                
                # Select the new step
                self.selected_step_index = insert_position
                self.step_listbox.selection_set(insert_position)
                
                # Notify callback
                if self.on_step_added:
                    self.on_step_added(new_step)
            
            # Show editor dialog
            editor = StepEditorDialog(
                self.parent,
                step_type,
                on_save,
                self._on_pick_coords if step_type in [StepType.CLICK, StepType.DOUBLE_CLICK, StepType.CLICK_AND_MOVE, StepType.SCREEN_LOADED] else None
            )
            
            # Set available columns if needed
            if step_type in [StepType.INSERT_COLUMN_VALUE, StepType.WRITE_TO_EXCEL] and self.available_columns:
                editor.set_columns(self.available_columns)
        
        # Show add step dialog
        AddStepDialog(self.parent, on_step_type_selected)
    
    def _on_pick_coords(self, callback: Callable[[int, int], None]) -> None:
        """Handle coordinate picker request"""
        from src.gui.coordinate_picker import CoordinatePicker
        
        picker = CoordinatePicker(self.parent, callback)
        picker.pick()
    
    def _on_move_up(self) -> None:
        """Handle Move Up button click"""
        if self.selected_step_index is None or self.selected_step_index == 0:
            return
        
        # Swap steps
        self.steps[self.selected_step_index], self.steps[self.selected_step_index - 1] = \
            self.steps[self.selected_step_index - 1], self.steps[self.selected_step_index]
        
        # Update orders
        self._reorder_steps()
        
        # Update display
        self._update_display()
        
        # Update selection
        self.selected_step_index -= 1
        self.step_listbox.selection_set(self.selected_step_index)
    
    def _on_move_down(self) -> None:
        """Handle Move Down button click"""
        if self.selected_step_index is None or self.selected_step_index >= len(self.steps) - 1:
            return
        
        # Swap steps
        self.steps[self.selected_step_index], self.steps[self.selected_step_index + 1] = \
            self.steps[self.selected_step_index + 1], self.steps[self.selected_step_index]
        
        # Update orders
        self._reorder_steps()
        
        # Update display
        self._update_display()
        
        # Update selection
        self.selected_step_index += 1
        self.step_listbox.selection_set(self.selected_step_index)
    
    def _on_delete_step(self) -> None:
        """Handle Delete Step button click"""
        if self.selected_step_index is None:
            messagebox.showwarning("No Selection", "Please select a step to delete")
            return
        
        # Confirm deletion
        step = self.steps[self.selected_step_index]
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Delete step: {self._format_step(step)}?"
        )
        
        if result:
            # Remove step
            del self.steps[self.selected_step_index]
            
            # Update orders
            self._reorder_steps()
            
            # Update display
            self._update_display()
            
            # Clear selection
            self.selected_step_index = None
    
    def _on_clear_all(self) -> None:
        """Handle Clear All button click"""
        if not self.steps:
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            f"Clear all {len(self.steps)} steps?"
        )
        
        if result:
            self.steps = []
            self.selected_step_index = None
            self._update_display()
    
    def _reorder_steps(self) -> None:
        """Update step order indices"""
        for i, step in enumerate(self.steps):
            step.order = i
    
    def _update_display(self) -> None:
        """Update the step list display"""
        self.step_listbox.delete(0, tk.END)
        
        for step in self.steps:
            self.step_listbox.insert(tk.END, self._format_step(step))
    
    def _format_step(self, step: WorkflowStep) -> str:
        """Format a step for display in the list"""
        step_type = step.type.value.replace('_', ' ').title()
        
        # Add key parameters
        if step.type == StepType.CLICK:
            params = f"({step.params.get('x', 0)}, {step.params.get('y', 0)})"
        elif step.type == StepType.DOUBLE_CLICK:
            params = f"({step.params.get('x', 0)}, {step.params.get('y', 0)})"
        elif step.type == StepType.TYPE_TEXT:
            text = step.params.get('text', '')
            params = f'"{text[:30]}...' if len(text) > 30 else f'"{text}"'
        elif step.type == StepType.WAIT:
            params = f"{step.params.get('duration_ms', 0)}ms"
        elif step.type == StepType.INSERT_COLUMN_VALUE:
            params = f"[{step.params.get('column_name', '')}]"
        elif step.type == StepType.PRESS_HOTKEY:
            params = f"[{step.params.get('hotkey', '')}]"
        elif step.type == StepType.CLICK_AND_MOVE:
            params = f"({step.params.get('start_x', '')}, {step.params.get('start_y', '')}) \u2192 ({step.params.get('end_x', '')}, {step.params.get('end_y', '')})"
        elif step.type == StepType.WRITE_TO_EXCEL:
            column = step.params.get('column_name', '')
            mode = "Mark Done" if step.params.get('write_mode', '') == "mark_done" else "Paste Clipboard"
            params = f"[{column}] ({mode})"
        elif step.type == StepType.SCREEN_LOADED:
            params = f"({step.params.get('start_x', '')}, {step.params.get('start_y', '')}) \u2192 ({step.params.get('end_x', '')}, {step.params.get('end_y', '')}) [max: {step.params.get('max_tries', '')}]"
        else:
            params = ""
        
        return f"{step.order + 1}. {step_type} {params}"
    
    def add_step(self, step: WorkflowStep) -> None:
        """
        Add a step to the workflow.
        
        Args:
            step: The step to add
        """
        self.steps.append(step)
        self._reorder_steps()
        self._update_display()
        
        # Select the new step
        self.selected_step_index = len(self.steps) - 1
        self.step_listbox.selection_set(self.selected_step_index)
    
    def get_workflow(self) -> Workflow:
        """
        Get the current workflow.
        
        Returns:
            Workflow object with current steps
        """
        return Workflow(
            name="Workflow",
            steps=self.steps.copy()
        )
    
    def set_workflow(self, workflow: Workflow) -> None:
        """
        Set the workflow and update display.
        
        Args:
            workflow: Workflow to load
        """
        self.steps = [WorkflowStep(
            type=step.type,
            order=step.order,
            params=step.params.copy()
        ) for step in workflow.steps]
        
        self._reorder_steps()
        self._update_display()
        self.selected_step_index = None
    
    def set_available_columns(self, columns: List[str]) -> None:
        """
        Set available columns for insert_column_value steps.
        
        Args:
            columns: List of column names
        """
        self.available_columns = columns
    
    def clear(self) -> None:
        """Clear all steps"""
        self.steps = []
        self.selected_step_index = None
        self._update_display()
    
    def has_steps(self) -> bool:
        """
        Check if workflow has any steps.
        
        Returns:
            True if steps exist, False otherwise
        """
        return len(self.steps) > 0
