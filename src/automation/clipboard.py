"""Clipboard operations for automation"""
import pyperclip


class ClipboardModule:
    """Module for clipboard operations"""
    
    def clear(self) -> None:
        """Clear the system clipboard by copying an empty string"""
        pyperclip.copy('')

    def paste(self) -> str:
        """Read and return the current clipboard content"""
        return pyperclip.paste()
