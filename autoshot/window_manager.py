"""
Window Manager Module
Handles window operations using Windows API
"""
import ctypes
from ctypes import wintypes
import time
from typing import Tuple, Optional


class WindowManager:
    def __init__(self):
        # Load required Windows API functions
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Define function signatures
        self.user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
        self.user32.FindWindowW.restype = wintypes.HWND
        self.user32.SetWindowPos.argtypes = [
            wintypes.HWND, wintypes.HWND,
            wintypes.INT, wintypes.INT,
            wintypes.INT, wintypes.INT,
            wintypes.UINT
        ]
        self.user32.SetWindowPos.restype = wintypes.BOOL
        self.user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
        self.user32.GetWindowRect.restype = wintypes.BOOL

    def find_window(self, class_name: Optional[str] = None, window_name: Optional[str] = None) -> Optional[int]:
        """
        Find a window by class name or window title
        
        Args:
            class_name: Window class name (optional)
            window_name: Window title (optional)
            
        Returns:
            Window handle or None if not found
        """
        hwnd = self.user32.FindWindowW(class_name, window_name)
        return hwnd if hwnd != 0 else None

    def resize_window(self, hwnd: int, width: int, height: int) -> bool:
        """
        Resize a window to specified dimensions
        
        Args:
            hwnd: Window handle
            width: Desired width
            height: Desired height
            
        Returns:
            True if successful, False otherwise
        """
        # SWP_NOZORDER | SWP_NOMOVE
        flags = 0x0004 | 0x0002
        result = self.user32.SetWindowPos(
            hwnd, 0, 0, 0, width, height, flags
        )
        return bool(result)

    def get_window_rect(self, hwnd: int) -> Optional[Tuple[int, int, int, int]]:
        """
        Get the rectangle coordinates of a window
        
        Args:
            hwnd: Window handle
            
        Returns:
            Tuple of (left, top, right, bottom) coordinates or None if failed
        """
        rect = wintypes.RECT()
        success = self.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        
        if success:
            return (rect.left, rect.top, rect.right, rect.bottom)
        return None

    def move_window_to_position(self, hwnd: int, x: int, y: int, width: int, height: int) -> bool:
        """
        Move and resize a window to a specific position
        
        Args:
            hwnd: Window handle
            x: X coordinate
            y: Y coordinate
            width: Width
            height: Height
            
        Returns:
            True if successful, False otherwise
        """
        flags = 0x0004  # SWP_NOZORDER
        result = self.user32.SetWindowPos(
            hwnd, 0, x, y, width, height, flags
        )
        return bool(result)