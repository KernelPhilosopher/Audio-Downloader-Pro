"""
Window Utilities Module

This module provides comprehensive utility functions for window management and system integration
in desktop applications. It encapsulates common window operations and system-specific features.

Key features:
- Window positioning and centering on screen
- Icon management and resource handling
- System-specific visual effects (Windows 10/11)
- Cross-platform downloads path resolution
- Custom UI shape generation

Dependencies:
- PIL (Python Imaging Library) for image processing
- ctypes for Windows API integration
- pathlib for cross-platform path handling
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageTk
import ctypes
from ctypes import windll


class WindowUtils:
    """
    A utility class providing window management and system operation functions.

    This class serves as a collection of static methods that handle various
    window-related operations and system integrations. It's designed to work
    across different platforms while providing enhanced functionality for
    Windows systems.

    Features:
    - Window positioning and dynamic resizing
    - Resource management (icons, images)
    - Windows-specific visual effects (Mica, Dark Mode)
    - Custom UI element generation
    - System path resolution

    Note: Some features are Windows-specific and will gracefully fallback
    on unsupported platforms.
    """

    @staticmethod
    def center(window, width_percentage=None, height_percentage=None):
        """
        Centers a window on the screen and optionally resizes it based on screen dimensions.

        This method calculates the optimal position for a window to appear centered
        on the screen. It can also adjust the window size based on screen percentages.

        Args:
            window: The window instance to be centered
            width_percentage (float, optional): Desired width as percentage of screen width
            height_percentage (float, optional): Desired height as percentage of screen height

        Example:
            center(main_window, 80, 60)  # Centers window at 80% width, 60% height
        """
        # Ensure window widgets are up to date
        window.update_idletasks()

        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Adjust window size if percentages are provided
        if width_percentage is not None and height_percentage is not None:
            window_width = int(screen_width * width_percentage / 100)
            window_height = int(screen_height * height_percentage / 100)
            window.geometry(f"{window_width}x{window_height}")
            window.update_idletasks()  # Update after resize
        else:
            window_width = window.winfo_width()
            window_height = window.winfo_height()

        # Calculate center position
        x = max(0, (screen_width // 2) - (window_width // 2))
        y = max(0, (screen_height // 2) - (window_height // 2))

        # Apply centered geometry
        window.geometry(f"+{x}+{y}")

    @staticmethod
    def set_window_icon(window, icon_name="app_icon"):
        """
        Sets the window icon from resources.

        This method attempts to set the window icon using a specified resource file.
        It supports both standard Python environments and frozen executables.

        Args:
            window: Target window for icon application
            icon_name (str): Name of the icon resource file (default: "app_icon")

        Returns:
            bool: True if the icon was successfully applied, False otherwise
        """
        try:
            # Attempt to use the standard path
            icon_path = os.path.join(
                os.path.dirname(__file__), "icons", f"{icon_name}.png"
            )

            # If running in a frozen executable
            if getattr(sys, "frozen", False) and not os.path.exists(icon_path):
                icon_path = os.path.join(sys._MEIPASS, "icons", f"{icon_name}.png")

            if os.path.exists(icon_path):
                icon = ImageTk.PhotoImage(Image.open(icon_path))
                window.iconphoto(True, icon)
                return True
        except Exception as e:
            print(f"Error setting the icon: {e}")
        return False

    @staticmethod
    def apply_window_blur(window):
        """
        Applies modern blur effect to window background (Windows 10/11 only).

        This method uses Windows API to apply visual effects like Mica or Dark Mode
        to the window background. It gracefully falls back on unsupported platforms.

        Args:
            window: Window to apply the effect to

        Returns:
            bool: True if the effect was successfully applied, False otherwise
        """
        try:
            if sys.platform == "win32":
                from ctypes import windll, c_int, byref, sizeof

                # Constants for Windows API
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_MICA_EFFECT = 1029

                # Reference to the window
                hwnd = windll.user32.GetParent(window.winfo_id())

                # Attempt to apply Mica effect (Windows 11)
                value = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_MICA_EFFECT, byref(value), sizeof(value)
                )
                return True
        except Exception:
            pass  # Silently fail if not supported
        return False

    @staticmethod
    def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
        """
        Creates a rounded rectangle shape on a canvas.

        This method generates a custom UI element with rounded corners
        on a given canvas.

        Args:
            canvas: Target canvas for shape creation
            x1, y1 (int): Top-left coordinates
            x2, y2 (int): Bottom-right coordinates
            radius (int): Corner radius (default: 20)
            **kwargs: Additional parameters for canvas drawing

        Returns:
            int: ID of the created shape
        """
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    @staticmethod
    def get_downloads_path() -> Path:
        """
        Determines the system's downloads directory path.

        This method resolves the path to the system's downloads directory
        in a cross-platform manner. It provides a fallback location if the
        resolution fails.

        Returns:
            Path: Path to the downloads directory or fallback location
        """
        try:
            if sys.platform == "win32":
                FOLDERID_Downloads = "{374DE290-123F-4565-9164-39C4925E467B}"
                psz_path = ctypes.c_wchar_p()
                hr = windll.shell32.SHGetKnownFolderPath(
                    ctypes.create_unicode_buffer(FOLDERID_Downloads),
                    0,
                    None,
                    ctypes.byref(psz_path),
                )
                if hr == 0:
                    path = Path(ctypes.wstring_at(psz_path))
                    windll.ole32.CoTaskMemFree(psz_path)
                else:
                    path = Path.home() / "Downloads"
            else:
                path = Path.home() / "Downloads"

            path.mkdir(parents=True, exist_ok=True)
            return path
        except Exception as e:
            fallback_path = Path.home() / "YT_Audio_Downloads"
            fallback_path.mkdir(exist_ok=True)
            return fallback_path
