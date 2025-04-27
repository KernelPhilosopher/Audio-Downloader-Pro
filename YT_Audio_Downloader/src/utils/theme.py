# YT_Audio_Downloader\src\utils\theme.py
import customtkinter as ctk
import os
import sys
from PIL import Image, ImageTk


class ProfessionalTheme:
    """
    A class to manage the professional theme settings of the application.
    This class provides methods for theme configuration, color management,
    and UI element styling.
    """

    # Color scheme definition for the entire application
    COLORS = {
        "background": "#1E1E2E",  # Main background color
        "foreground": "#252538",  # Secondary background color
        "accent": "#5D78FF",  # Primary accent color for interactive elements
        "accent_hover": "#4A63D2",  # Hover state color for interactive elements
        "success": "#5CE592",  # Color for success states and messages
        "error": "#FF5D6C",  # Color for error states and messages
        "warning": "#FFB86C",  # Color for warning states and messages
        "text": "#E0E1F0",  # Primary text color
        "text_muted": "#979DAC",  # Secondary text color for less emphasis
    }

    @classmethod
    def apply(cls):
        """
        Applies the theme configuration to the application.
        This includes setting the appearance mode, color theme,
        and configuring default fonts for different UI elements.
        """
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme(cls._get_theme_path())

        # Configure default fonts for UI elements
        ctk.CTkLabel._font = ("Segoe UI", 11)
        ctk.CTkButton._font = ("Segoe UI", 11, "bold")
        ctk.CTkTextbox._font = ("Consolas", 11)
        ctk.CTkOptionMenu._font = ("Segoe UI", 11)

    @classmethod
    def _get_theme_path(cls):
        """
        Retrieves the path to the theme.json file.

        Returns:
            str or None: The path to the theme.json file if found, None otherwise.

        Note:
            The method checks both the regular file system path and
            PyInstaller's temporary directory when running as a frozen application.
        """
        base_path = os.path.dirname(__file__)
        paths_to_try = [
            os.path.join(base_path, "theme.json"),
            (
                os.path.join(sys._MEIPASS, "theme.json")
                if getattr(sys, "frozen", False)
                else None
            ),
        ]

        for path in paths_to_try:
            if path and os.path.exists(path):
                return path
        return None

    @classmethod
    def get_icon(cls, icon_name, size=(24, 24)):
        """
        Loads and returns an icon from the resources directory.

        Args:
            icon_name (str): The name of the icon file without extension
            size (tuple): The desired size of the icon as (width, height)

        Returns:
            ImageTk.PhotoImage or None: The loaded and resized icon, or None if loading fails
        """
        try:
            icon_path = os.path.join(
                os.path.dirname(__file__), "icons", f"{icon_name}.png"
            )
            return ImageTk.PhotoImage(Image.open(icon_path).resize(size))
        except Exception as e:
            print(f"Error loading icon {icon_name}: {e}")
            return None

    @classmethod
    def apply_scrollbar_style(cls, scrollbar):
        """
        Applies custom styling to scrollbar widgets.

        Args:
            scrollbar (ctk.CTkScrollbar): The scrollbar widget to style

        Note:
            Configures the scrollbar's width, colors, and hover states
            to match the application's theme.
        """
        scrollbar.configure(
            width=12,
            trough_color=cls.COLORS["background"],
            button_color=cls.COLORS["accent"],
            button_hover_color=cls.COLORS["accent_hover"],
        )
