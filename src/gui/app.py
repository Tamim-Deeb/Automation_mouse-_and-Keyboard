"""Main application window with three-panel layout"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.gui.theme import COLOR_DARK_HEADER, COLOR_LIGHT_PANEL, COLOR_TEXT_LIGHT


class App:
    """
    Main application window for the Excel-Driven Desktop Automation Workflow Builder.
    Three-panel layout: Excel panel (top), Workflow panel (center), Execution panel (bottom).
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main application window.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Automation Mouse & Keyboard v1.0")
        self.root.geometry("1000x800")
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create main container with three panels
        self._create_panels()
    
    def _create_menu_bar(self) -> None:
        """Create the application menu bar"""
        menubar = tk.Menu(self.root, bg=COLOR_DARK_HEADER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_DARK_HEADER, activeforeground=COLOR_TEXT_LIGHT)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=COLOR_DARK_HEADER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_DARK_HEADER, activeforeground=COLOR_TEXT_LIGHT)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Workflow", command=self._on_new_workflow)
        file_menu.add_command(label="Open Workflow...", command=self._on_open_workflow)
        file_menu.add_command(label="Save Workflow", command=self._on_save_workflow)
        file_menu.add_command(label="Save Workflow As...", command=self._on_save_workflow_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_exit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=COLOR_DARK_HEADER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_DARK_HEADER, activeforeground=COLOR_TEXT_LIGHT)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._on_about)
    
    def _create_panels(self) -> None:
        """Create the three-panel layout"""
        # Main container with vertical layout
        main_container = ttk.Frame(self.root, padding="10", style="Light.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Excel panel (top) - for importing and selecting Excel data
        self.excel_panel = ttk.LabelFrame(main_container, text="Excel Data Source", padding="10", style="Styled.TLabelframe")
        self.excel_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Placeholder content for Excel panel
        excel_content = ttk.Frame(self.excel_panel)
        excel_content.pack(fill=tk.X)
        
        ttk.Label(excel_content, text="Import Excel file to begin").pack(side=tk.LEFT, padx=5)
        self.import_excel_btn = ttk.Button(excel_content, text="Import Excel", command=self._on_import_excel, style="Custom.TButton")
        self.import_excel_btn.pack(side=tk.LEFT, padx=5)
        
        # Workflow panel (center) - for building and managing steps
        self.workflow_panel = ttk.LabelFrame(main_container, text="Workflow Steps", padding="10", style="Styled.TLabelframe")
        self.workflow_panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Placeholder content for Workflow panel
        workflow_content = ttk.Frame(self.workflow_panel)
        workflow_content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(workflow_content, text="No steps added yet").pack(pady=20)
        self.add_step_btn = ttk.Button(workflow_content, text="Add Step", command=self._on_add_step, style="Custom.TButton")
        self.add_step_btn.pack(pady=5)
        
        # Execution panel (bottom) - for starting/stopping execution
        self.execution_panel = ttk.LabelFrame(main_container, text="Execution", padding="10", style="Styled.TLabelframe")
        self.execution_panel.pack(fill=tk.X)
        
        # Placeholder content for Execution panel
        execution_content = ttk.Frame(self.execution_panel)
        execution_content.pack(fill=tk.X)
        
        ttk.Label(execution_content, text="Start Row:").pack(side=tk.LEFT, padx=5)
        self.start_row_entry = ttk.Entry(execution_content, width=10)
        self.start_row_entry.insert(0, "1")
        self.start_row_entry.pack(side=tk.LEFT, padx=5)
        
        self.dry_run_var = tk.BooleanVar(value=False)
        self.dry_run_chk = ttk.Checkbutton(execution_content, text="Dry Run", variable=self.dry_run_var)
        self.dry_run_chk.pack(side=tk.LEFT, padx=10)
        
        self.start_btn = ttk.Button(execution_content, text="Start", command=self._on_start, style="Custom.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(execution_content, text="Stop", command=self._on_stop, state=tk.DISABLED, style="Custom.TButton")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.progress_label = ttk.Label(execution_content, text="Ready")
        self.progress_label.pack(side=tk.RIGHT, padx=10)
    
    # Menu handlers
    def _on_new_workflow(self) -> None:
        """Handle New Workflow menu command"""
        messagebox.showinfo("New Workflow", "Create a new workflow (placeholder)")
    
    def _on_open_workflow(self) -> None:
        """Handle Open Workflow menu command"""
        file_path = filedialog.askopenfilename(
            title="Open Workflow",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Open Workflow", f"Opening workflow: {file_path}")
    
    def _on_save_workflow(self) -> None:
        """Handle Save Workflow menu command"""
        messagebox.showinfo("Save Workflow", "Save workflow (placeholder)")
    
    def _on_save_workflow_as(self) -> None:
        """Handle Save Workflow As menu command"""
        file_path = filedialog.asksaveasfilename(
            title="Save Workflow As",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Save Workflow As", f"Saving workflow to: {file_path}")
    
    def _on_exit(self) -> None:
        """Handle Exit menu command"""
        self.root.quit()
    
    def _on_about(self) -> None:
        """Handle About menu command"""
        messagebox.showinfo(
            "About",
            "Excel-Driven Desktop Automation Workflow Builder\n\n"
            "Build automation workflows visually and execute them row-by-row against Excel data."
        )
    
    # Panel handlers
    def _on_import_excel(self) -> None:
        """Handle Import Excel button click"""
        file_path = filedialog.askopenfilename(
            title="Import Excel File",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Import Excel", f"Imported: {file_path}")
    
    def _on_add_step(self) -> None:
        """Handle Add Step button click"""
        messagebox.showinfo("Add Step", "Add a workflow step (placeholder)")
    
    def _on_start(self) -> None:
        """Handle Start button click"""
        messagebox.showinfo("Start", "Start execution (placeholder)")
    
    def _on_stop(self) -> None:
        """Handle Stop button click"""
        messagebox.showinfo("Stop", "Stop execution (placeholder)")
    
    def run(self) -> None:
        """Start the application main loop"""
        self.root.mainloop()


def main():
    """Entry point for the application"""
    root = tk.Tk()
    app = App(root)
    app.run()


if __name__ == "__main__":
    main()
