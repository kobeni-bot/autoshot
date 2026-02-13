"""
Window Manager Module
Handles window operations using Windows API
"""
import ctypes
from ctypes import wintypes
import time
from typing import Tuple, Optional, Union


class WindowManager:
    def __init__(self):
        # Load required Windows API functions
        self.user32 = ctypes.windll.user32
        self.gdi32 = ctypes.windll.gdi32
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
        self.user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
        self.user32.GetClientRect.restype = wintypes.BOOL
        self.user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
        self.user32.ClientToScreen.restype = wintypes.BOOL
        self.user32.GetDC.argtypes = [wintypes.HWND]
        self.user32.GetDC.restype = wintypes.HDC
        self.user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
        self.user32.ReleaseDC.restype = ctypes.c_int
        self.gdi32.GetPixel.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]
        self.gdi32.GetPixel.restype = wintypes.COLORREF

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

    def get_client_rect(self, hwnd: int) -> Optional[Tuple[int, int, int, int]]:
        """
        Get the client rectangle coordinates of a window (excluding borders and title bar)
        
        Args:
            hwnd: Window handle
            
        Returns:
            Tuple of (left, top, right, bottom) client coordinates or None if failed
        """
        # First get the client rectangle (relative to client area)
        client_rect = wintypes.RECT()
        success = self.user32.GetClientRect(hwnd, ctypes.byref(client_rect))
        
        if not success:
            return None

        # Convert client coordinates to screen coordinates
        # Top-left corner
        point_topleft = wintypes.POINT(client_rect.left, client_rect.top)
        self.user32.ClientToScreen(hwnd, ctypes.byref(point_topleft))
        
        # Bottom-right corner
        point_bottomright = wintypes.POINT(client_rect.right, client_rect.bottom)
        self.user32.ClientToScreen(hwnd, ctypes.byref(point_bottomright))
        
        # Return the absolute screen coordinates
        return (
            point_topleft.x,
            point_topleft.y,
            point_bottomright.x,
            point_bottomright.y
        )

    def get_pixel_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """
        Get the RGB color of a pixel at the specified screen coordinates
        
        Args:
            x: X coordinate on screen
            y: Y coordinate on screen
            
        Returns:
            Tuple of (R, G, B) values or None if failed
        """
        # Get device context for the screen
        hdc = self.user32.GetDC(None)
        if not hdc:
            return None

        try:
            # Get the pixel color
            color = self.gdi32.GetPixel(hdc, x, y)
            if color == 0xFFFFFFFF:  # Error value
                return None

            # Extract RGB components from COLORREF
            r = color & 0xFF
            g = (color >> 8) & 0xFF
            b = (color >> 16) & 0xFF

            return (r, g, b)
        finally:
            # Release the device context
            self.user32.ReleaseDC(None, hdc)

    def convert_screenshot_coords_to_screen(self, hwnd: int, screenshot_x: int, screenshot_y: int, use_client_area: bool = True) -> Optional[Tuple[int, int]]:
        """
        Convert coordinates from a screenshot to screen coordinates
        
        Args:
            hwnd: Window handle
            screenshot_x: X coordinate in the screenshot
            screenshot_y: Y coordinate in the screenshot
            use_client_area: Whether to use client area (True) or full window (False)
            
        Returns:
            Tuple of (screen_x, screen_y) coordinates or None if failed
        """
        # Get the window/client rectangle depending on the flag
        if use_client_area:
            rect = self.get_client_rect(hwnd)
        else:
            rect = self.get_window_rect(hwnd)
        
        if rect is None:
            return None
            
        left, top, _, _ = rect
        # Calculate the screen coordinates
        screen_x = left + screenshot_x
        screen_y = top + screenshot_y
        
        return (screen_x, screen_y)

    def get_pixel_from_screenshot_coords(self, hwnd: int, screenshot_x: int, screenshot_y: int, use_client_area: bool = True) -> Optional[Tuple[int, int, int]]:
        """
        Get the RGB color of a pixel based on screenshot coordinates
        
        Args:
            hwnd: Window handle
            screenshot_x: X coordinate in the screenshot
            screenshot_y: Y coordinate in the screenshot
            use_client_area: Whether to use client area (True) or full window (False)
            
        Returns:
            Tuple of (R, G, B) values or None if failed
        """
        # Convert screenshot coordinates to screen coordinates
        screen_coords = self.convert_screenshot_coords_to_screen(hwnd, screenshot_x, screenshot_y, use_client_area)
        if screen_coords is None:
            return None
            
        screen_x, screen_y = screen_coords
        return self.get_pixel_color(screen_x, screen_y)

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