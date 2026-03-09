"""Excel panel GUI for importing and selecting Excel data"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable
from src.excel.reader import ExcelReader


class ExcelPanel:
    """
    Panel for importing Excel files and selecting worksheets.
    Displays column headers and row count.
    """
    
    def __init__(self, parent: ttk.Frame, on_data_loaded: Optional[Callable] = None):
        """
        Initialize the Excel panel.
        
        Args:
            parent: Parent widget
            on_data_loaded: Callback function when Excel data is loaded
        """
        self.parent = parent
        self.on_data_loaded = on_data_loaded
        
        self.file_path: Optional[str] = None
        self.sheet_names: list[str] = []
        self.selected_sheet: Optional[str] = None
        self.headers: list[str] = []
        self.row_count: int = 0
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create the panel widgets"""
        # Import button
        self.import_btn = ttk.Button(
            self.parent,
            text="Import Excel",
            command=self._on_import_excel
        )
        self.import_btn.pack(side=tk.LEFT, padx=5)
        
        # File path label
        self.file_label = ttk.Label(self.parent, text="No file imported")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Sheet selection dropdown
        ttk.Label(self.parent, text="Sheet:").pack(side=tk.LEFT, padx=(10, 2))
        self.sheet_var = tk.StringVar()
        self.sheet_dropdown = ttk.OptionMenu(
            self.parent,
            self.sheet_var,
            "",
            *[]
        )
        self.sheet_dropdown.pack(side=tk.LEFT, padx=5)
        self.sheet_dropdown.configure(state=tk.DISABLED)
        
        # Bind selection change
        self.sheet_var.trace_add('write', self._on_sheet_changed)
        
        # Headers display
        self.headers_frame = ttk.LabelFrame(self.parent, text="Column Headers", padding="5")
        self.headers_frame.pack(side=tk.LEFT, padx=(10, 5), fill=tk.Y)
        
        self.headers_listbox = tk.Listbox(
            self.headers_frame,
            height=5,
            width=30
        )
        self.headers_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Row count display
        self.row_count_label = ttk.Label(self.parent, text="Rows: 0")
        self.row_count_label.pack(side=tk.LEFT, padx=10)
    
    def _on_import_excel(self) -> None:
        """Handle Import Excel button click"""
        file_path = filedialog.askopenfilename(
            title="Import Excel File",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Load the workbook
            with ExcelReader(file_path) as reader:
                sheet_names = reader.load_workbook()
            
            # Update UI
            self.file_path = file_path
            self.sheet_names = sheet_names
            self.file_label.config(text=file_path.split("/")[-1])
            
            # Update sheet dropdown
            self.sheet_var.set("")
            menu = self.sheet_dropdown["menu"]
            menu.delete(0, tk.END)
            
            for sheet_name in sheet_names:
                menu.add_command(
                    label=sheet_name,
                    command=lambda name=sheet_name: self._select_sheet(name)
                )
            
            self.sheet_dropdown.configure(state=tk.NORMAL)
            
            # Clear previous data
            self.selected_sheet = None
            self.headers = []
            self.row_count = 0
            self._update_headers_display()
            self.row_count_label.config(text="Rows: 0")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import Excel file:\n{e}")
    
    def _select_sheet(self, sheet_name: str) -> None:
        """Select a sheet from the dropdown"""
        self.sheet_var.set(sheet_name)
    
    def _on_sheet_changed(self, *args) -> None:
        """Handle sheet selection change"""
        sheet_name = self.sheet_var.get()
        
        if not sheet_name or not self.file_path:
            return
        
        try:
            # Load sheet data
            with ExcelReader(self.file_path) as reader:
                reader.load_workbook()
                reader.select_sheet(sheet_name)
                
                self.selected_sheet = sheet_name
                self.headers = reader.get_headers()
                self.row_count = reader.get_row_count()
            
            # Update UI
            self._update_headers_display()
            self.row_count_label.config(text=f"Rows: {self.row_count}")
            
            # Notify callback
            if self.on_data_loaded:
                self.on_data_loaded(self.headers, self.row_count)
            
        except Exception as e:
            messagebox.showerror("Sheet Error", f"Failed to load sheet:\n{e}")
    
    def _update_headers_display(self) -> None:
        """Update the headers listbox"""
        self.headers_listbox.delete(0, tk.END)
        
        for header in self.headers:
            self.headers_listbox.insert(tk.END, header)
    
    def get_data_source(self) -> Optional[dict]:
        """
        Get the current Excel data source information.
        
        Returns:
            Dictionary with file_path, sheet_name, headers, row_count, or None if no data loaded
        """
        if not self.file_path or not self.selected_sheet:
            return None
        
        return {
            "file_path": self.file_path,
            "sheet_name": self.selected_sheet,
            "headers": self.headers,
            "row_count": self.row_count
        }
    
    def is_data_loaded(self) -> bool:
        """
        Check if Excel data is loaded.
        
        Returns:
            True if data is loaded, False otherwise
        """
        return bool(self.file_path and self.selected_sheet)
    
    def clear(self) -> None:
        """Clear all loaded data"""
        self.file_path = None
        self.sheet_names = []
        self.selected_sheet = None
        self.headers = []
        self.row_count = 0
        
        self.file_label.config(text="No file imported")
        self.sheet_var.set("")
        self.sheet_dropdown.configure(state=tk.DISABLED)
        self._update_headers_display()
        self.row_count_label.config(text="Rows: 0")
