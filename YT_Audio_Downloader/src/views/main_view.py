"""
Main View Module

This module implements the main graphical user interface for the YouTube Audio Downloader
using the customtkinter framework. It provides a modern, responsive UI with features like:

Features:
- URL input for multiple YouTube links
- Audio format selection
- Download progress tracking
- Activity logging
- Legal compliance checks
- Modern dark theme with accent colors
- Help and documentation access
- Error handling and user notifications

The MainView class inherits from CTk and implements DownloadObserver to handle
download status updates in real-time.
"""

# YT_Audio_Downloader\src\views\main_view.py
import customtkinter as ctk
import tkinter as tk
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
import os
from models import DownloadObserver
from utils import ProfessionalTheme, WindowUtils


class MainView(ctk.CTk, DownloadObserver):
    """
    Main graphical interface enhanced with professional design.
    Implements DownloadObserver to receive download status updates.

    This class builds and manages the entire UI of the application, including:
    - URL input area for YouTube links
    - Format selection and download controls
    - Progress tracking and status display
    - Activity log
    - Legal compliance controls
    """

    def __init__(self, controller):
        """
        Initialize the main window and set up all UI components.

        Args:
            controller: Reference to the application controller
        """
        super().__init__()

        # Main attributes
        self.controller = controller
        self.current_task = None
        self.legal_checkbox_var = ctk.BooleanVar(value=False)

        # Initial configurations
        ProfessionalTheme.apply()
        self._configure_window()
        self._create_widgets()
        self._setup_layout()
        self._configure_styles()

        # Center window with optimized proportions
        WindowUtils.center(self, width_percentage=65, height_percentage=70)

        # Load application icon
        WindowUtils.set_window_icon(self)

        # Show initial disclaimer
        self._show_disclaimer()

    def _configure_window(self):
        """Configure the main window properties and appearance"""
        self.title("Audio Downloader Pro")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Try to apply modern visual effect on Windows
        WindowUtils.apply_window_blur(self)

    def _create_widgets(self):
        """Create all UI widgets with their initial properties"""
        # Main frame with internal padding
        self.main_frame = ctk.CTkFrame(self)

        # Top bar with logo and information
        self.header_frame = self._create_header_frame()

        # URL input section
        self.input_frame = self._create_input_frame()

        # Controls and format section
        self.controls_frame = self._create_controls_frame()

        # Current progress section
        self.progress_frame = self._create_progress_frame()

        # Log section
        self.log_frame = self._create_log_frame()

        # Footer with legal information and links
        self.footer_frame = self._create_footer_frame()

    def _create_header_frame(self):
        """Create top bar with logo and information"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

        # Logo (stylized text)
        logo_label = ctk.CTkLabel(
            frame,
            text="🎵 Audio Downloader Pro",
            font=("Segoe UI", 18, "bold"),
            text_color=ProfessionalTheme.COLORS["accent"],
        )
        logo_label.pack(side="left", padx=5)

        # Help button
        help_btn = ctk.CTkButton(
            frame,
            text="?",
            width=30,
            height=30,
            corner_radius=15,
            font=("Segoe UI", 14, "bold"),
            command=self._show_help,
        )
        help_btn.pack(side="right", padx=5)

        return frame

    def _create_input_frame(self):
        """Create URL input section"""
        frame = ctk.CTkFrame(self.main_frame)

        # Instructions label
        input_label = ctk.CTkLabel(
            frame,
            text="Enter YouTube URLs (one per line):",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        )
        input_label.pack(fill="x", padx=10, pady=(10, 5))

        # URL input field
        self.url_input = ctk.CTkTextbox(
            frame, height=100, wrap="word", font=("Consolas", 12)
        )
        self.url_input.pack(fill="x", padx=10, pady=5)

        # Usage examples
        example_label = ctk.CTkLabel(
            frame,
            text="Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            font=("Segoe UI", 10),
            text_color=ProfessionalTheme.COLORS["text_muted"],
            anchor="w",
        )
        example_label.pack(fill="x", padx=10, pady=(0, 10))

        return frame

    def _create_controls_frame(self):
        """Create controls and format section"""
        frame = ctk.CTkFrame(self.main_frame)

        # Internal container for better spacing
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=10, pady=10)

        # Format selector with label
        format_label = ctk.CTkLabel(
            inner_frame, text="Format:", font=("Segoe UI", 12), width=70
        )
        format_label.pack(side="left", padx=(5, 0))

        self.format_selector = ctk.CTkOptionMenu(
            inner_frame,
            values=["MP3 320kbps", "MP3 192kbps", "WAV", "M4A", "OGG"],
            font=("Segoe UI", 12),
            width=150,
        )
        self.format_selector.pack(side="left", padx=10)
        self.format_selector.set("MP3 320kbps")

        # Download button
        self.download_btn = ctk.CTkButton(
            inner_frame,
            text="Start Downloads",
            font=("Segoe UI", 12, "bold"),
            command=self.controller.start_downloads,
            width=200,
            height=35,
            corner_radius=8,
        )
        self.download_btn.pack(side="right", padx=10)

        # Legal checkbox
        self.legal_check = ctk.CTkCheckBox(
            inner_frame,
            text="I accept legal terms",
            variable=self.legal_checkbox_var,
            font=("Segoe UI", 11),
            checkbox_width=20,
            checkbox_height=20,
        )
        self.legal_check.pack(side="right", padx=10)

        return frame

    def _create_progress_frame(self):
        """Create current progress section"""
        frame = ctk.CTkFrame(self.main_frame)

        # Internal container for better spacing
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=15, pady=10)

        # Current download information
        self.status_label = ctk.CTkLabel(
            inner_frame,
            text="Status: Ready to download",
            font=("Segoe UI", 11),
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(0, 5))

        # Progress bar
        progress_container = ctk.CTkFrame(inner_frame, fg_color="transparent")
        progress_container.pack(fill="x", pady=5)

        self.progress_bar = ctk.CTkProgressBar(
            progress_container, height=15, corner_radius=7
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.progress_bar.set(0)

        # Numeric percentage
        self.progress_percent = ctk.CTkLabel(
            progress_container, text="0%", font=("Segoe UI", 11), width=40
        )
        self.progress_percent.pack(side="right")

        return frame

    def _create_log_frame(self):
        """Create activity log section"""
        frame = ctk.CTkFrame(self.main_frame)

        # Section label
        log_label = ctk.CTkLabel(
            frame,
            text="Activity Log:",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        )
        log_label.pack(fill="x", padx=10, pady=(10, 5))

        # Log text field
        self.log_display = ctk.CTkTextbox(
            frame, state="disabled", wrap="word", font=("Consolas", 11)
        )
        self.log_display.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        return frame

    def _create_footer_frame(self):
        """Create footer with legal information and links"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=30)

        # Version information
        version_label = ctk.CTkLabel(
            frame,
            text="v1.0.0",
            font=("Segoe UI", 10),
            text_color=ProfessionalTheme.COLORS["text_muted"],
        )
        version_label.pack(side="right", padx=10)

        # Terms link
        terms_link = ctk.CTkLabel(
            frame,
            text="Terms and Conditions",
            font=("Segoe UI", 10, "underline"),
            text_color=ProfessionalTheme.COLORS["accent"],
            cursor="hand2",
        )
        terms_link.pack(side="left", padx=10)
        terms_link.bind("<Button-1>", lambda e: self._show_disclaimer())

        return frame

    def _setup_layout(self):
        """Organize all frames in the main window"""
        # Main frame occupies the entire window with padding
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Vertical arrangement of sections
        self.header_frame.pack(fill="x", pady=(0, 15))
        self.input_frame.pack(fill="x", pady=5)
        self.controls_frame.pack(fill="x", pady=5)
        self.progress_frame.pack(fill="x", pady=5)
        self.log_frame.pack(fill="both", expand=True, pady=5)
        self.footer_frame.pack(fill="x", pady=(5, 0))

    def _configure_styles(self):
        """Configure additional styles and visual details"""
        # Specific font configurations
        self.url_input.configure(font=("Consolas", 12))
        self.log_display.configure(font=("Consolas", 11))

        # Add initial message to the log
        self._append_log("✨ Application started. Ready to download.")

    def _show_disclaimer(self):
        """Displays the terms and conditions dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Terms and Conditions")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        # Block interaction with the main window
        dialog.grab_set()
        dialog.transient(self)

        # Main frame with improved design
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Header with title
        header = ctk.CTkLabel(
            main_frame,
            text="Terms and Conditions of Use",
            font=("Segoe UI", 16, "bold"),
            text_color=ProfessionalTheme.COLORS["accent"],
        )
        header.pack(pady=(10, 20))

        # Terms content in scrollable frame
        terms_frame = ctk.CTkScrollableFrame(main_frame, height=250)
        terms_frame.pack(fill="x", padx=10, pady=10)

        terms_text = """
        TERMS AND CONDITIONS OF USE
        
        1. USER RESPONSIBILITY
        
        This application is designed exclusively for downloading content that you own the rights to or are authorized to download. The user is fully responsible for the use of this tool.
        
        2. LEGAL USE
        
        You agree to use this application only for legal purposes and in accordance with copyright laws applicable in your jurisdiction. Downloading protected content without authorization may constitute a copyright violation.
        
        3. LIMITATION OF LIABILITY
        
        The developers of this application are not responsible for any misuse of this tool. This application is provided "as is," without any warranties.
        
        4. PRIVACY
        
        This application does not collect or store personal information from the user or activity logs on external servers.
        
        5. UPDATES
        
        Terms may be updated periodically. It is the user's responsibility to review these terms regularly.
        """

        terms_label = ctk.CTkLabel(
            terms_frame,
            text=terms_text,
            font=("Segoe UI", 11),
            justify="left",
            wraplength=540,
        )
        terms_label.pack(fill="both", padx=5, pady=5)

        # Links
        links_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        links_frame.pack(fill="x", padx=10, pady=(15, 5))

        # Interactive link
        terms_link = ctk.CTkLabel(
            links_frame,
            text="📄 View Full Documentation",
            text_color=ProfessionalTheme.COLORS["accent"],
            font=("Segoe UI", 11, "underline"),
            cursor="hand2",
        )
        terms_link.pack(side="left")
        terms_link.bind(
            "<Button-1>", lambda e: webbrowser.open("https://example.com/terms.pdf")
        )

        # Acceptance button
        accept_btn = ctk.CTkButton(
            main_frame,
            text="I Accept the Terms",
            command=lambda: (self.legal_checkbox_var.set(True), dialog.destroy()),
            fg_color=ProfessionalTheme.COLORS["success"],
            hover_color="#4BB280",
            width=200,
            height=35,
        )
        accept_btn.pack(pady=15)

        # Center dialog
        WindowUtils.center(dialog)

    def _show_help(self):
        """Displays the help dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Help")
        dialog.geometry("500x350")
        dialog.resizable(False, False)

        # Block interaction with the main window
        dialog.grab_set()
        dialog.transient(self)

        # Main frame
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🔍 Quick Help",
            font=("Segoe UI", 16, "bold"),
            text_color=ProfessionalTheme.COLORS["accent"],
        )
        title.pack(pady=(10, 20))

        # Help content
        help_frame = ctk.CTkScrollableFrame(main_frame)
        help_frame.pack(fill="both", expand=True, padx=10, pady=10)

        help_sections = [
            {
                "title": "How to download audio",
                "content": "1. Paste one or more YouTube URLs\n2. Select the desired format\n3. Accept the legal terms\n4. Click 'Start Downloads'",
            },
            {
                "title": "Available formats",
                "content": "• MP3 320kbps - High quality, larger size\n• MP3 192kbps - Good quality, medium size\n• WAV - Lossless quality, large size\n• M4A - Apple format, good quality\n• OGG - Free format, good quality",
            },
            {
                "title": "Troubleshooting",
                "content": "• Ensure you have an internet connection\n• Verify that FFmpeg is installed\n• URLs must be valid YouTube links\n• Check the log for specific errors",
            },
        ]

        for i, section in enumerate(help_sections):
            # Section title
            section_title = ctk.CTkLabel(
                help_frame,
                text=section["title"],
                font=("Segoe UI", 12, "bold"),
                text_color=ProfessionalTheme.COLORS["accent"],
                anchor="w",
            )
            section_title.pack(fill="x", padx=5, pady=(10 if i > 0 else 0, 5))

            # Section content
            section_content = ctk.CTkLabel(
                help_frame,
                text=section["content"],
                font=("Segoe UI", 11),
                justify="left",
                anchor="w",
                wraplength=450,
            )
            section_content.pack(fill="x", padx=15, pady=5)

        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=dialog.destroy,
            width=120,
            height=32,
        )
        close_btn.pack(pady=15)

        # Center dialog
        WindowUtils.center(dialog)

    def show_warning(self, title, message):
        """Displays a warning to the user"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        # Block interaction with the main window
        dialog.grab_set()
        dialog.transient(self)

        # Main frame
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Warning icon (emoji)
        warning_label = ctk.CTkLabel(
            main_frame,
            text="⚠️",
            font=("Segoe UI", 36),
            text_color=ProfessionalTheme.COLORS["warning"],
        )
        warning_label.pack(pady=(10, 5))

        # Message
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=("Segoe UI", 12),
            wraplength=350,
            justify="center",
        )
        message_label.pack(pady=15, padx=10)

        # Accept button
        ok_btn = ctk.CTkButton(
            main_frame,
            text="Understood",
            command=dialog.destroy,
            width=120,
            height=32,
        )
        ok_btn.pack(pady=10)

        # Center dialog
        WindowUtils.center(dialog)

    def show_error(self, message, title="Error"):
        """Displays an error message to the user"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        # Block interaction with the main window
        dialog.grab_set()
        dialog.transient(self)

        # Main frame
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Error icon (emoji)
        error_label = ctk.CTkLabel(
            main_frame,
            text="❌",
            font=("Segoe UI", 36),
            text_color=ProfessionalTheme.COLORS["error"],
        )
        error_label.pack(pady=(10, 5))

        # Message
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=("Segoe UI", 12),
            wraplength=350,
            justify="center",
        )
        message_label.pack(pady=15, padx=10)

        # Accept button
        ok_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=dialog.destroy,
            width=120,
            height=32,
            fg_color=ProfessionalTheme.COLORS["error"],
            hover_color="#D64A55",
        )
        ok_btn.pack(pady=10)

        # Center dialog
        WindowUtils.center(dialog)

        # Add to log
        self._append_log(f"❌ ERROR: {message}")

    def _append_log(self, message):
        """Adds a message to the activity log with a timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        # Enable editing, insert text, and disable editing again
        self.log_display.configure(state="normal")
        self.log_display.insert("end", log_entry)
        self.log_display.see("end")  # Auto-scroll to the end
        self.log_display.configure(state="disabled")

    def _update_progress_ui(self, task):
        """Updates the progress UI with task information"""
        # Update status label
        status_text = f"Status: {task.status} - {os.path.basename(task.url)}"
        self.status_label.configure(text=status_text)

        # Update progress bar
        progress_value = task.progress / 100.0
        self.progress_bar.set(progress_value)

        # Update percentage label
        self.progress_percent.configure(text=f"{int(task.progress)}%")

        # Update progress bar color based on status
        if task.status == "Error":
            self.progress_bar.configure(
                progress_color=ProfessionalTheme.COLORS["error"]
            )
        elif task.status == "Completed":
            self.progress_bar.configure(
                progress_color=ProfessionalTheme.COLORS["success"]
            )
        else:
            self.progress_bar.configure(
                progress_color=ProfessionalTheme.COLORS["accent"]
            )

    def on_progress_update(self, task):
        """Updates the UI with download progress (Implementation of DownloadObserver)"""
        self.current_task = task
        self._update_progress_ui(task)

    def on_task_complete(self, task):
        """Handles successful task completion (Implementation of DownloadObserver)"""
        self.current_task = task
        self._update_progress_ui(task)
        self._append_log(f"✅ Download completed: {os.path.basename(task.url)}")

    def on_task_error(self, task):
        """Handles errors in the download task (Implementation of DownloadObserver)"""
        self.current_task = task
        self._update_progress_ui(task)
        self._append_log(
            f"❌ Download error: {os.path.basename(task.url)} - {task.error}"
        )

    def get_urls(self):
        """Gets the list of URLs from the text field"""
        text_content = self.url_input.get("1.0", "end-1c").strip()
        if not text_content:
            return []

        # Split by line breaks and filter empty lines
        urls = [url.strip() for url in text_content.split("\n") if url.strip()]
        return urls

    def get_format(self):
        """Gets the selected format in a suitable format for yt-dlp"""
        format_map = {
            "MP3 320kbps": "mp3",
            "MP3 192kbps": "mp3",
            "WAV": "wav",
            "M4A": "m4a",
            "OGG": "vorbis",
        }

        selected = self.format_selector.get()
        return format_map.get(selected, "mp3")

    def legal_accepted(self):
        """Checks if the user accepted the legal terms"""
        return self.legal_checkbox_var.get()

    def mainloop(self):
        """Starts the application's main loop"""
        self.after(100, self._check_ffmpeg)  # Check dependencies after starting
        super().mainloop()

    def _check_ffmpeg(self):
        """Checks the availability of FFmpeg at startup"""
        # Already checked in the controller, this method is for future extensions
        pass

    def _on_closing(self):
        """Handles the window closing event"""
        # Ask if there are downloads in progress
        if self.current_task and self.current_task.status == "Downloading":
            dialog = ctk.CTkToplevel(self)
            dialog.title("Confirm Exit")
            dialog.geometry("400x200")
            dialog.resizable(False, False)
            dialog.grab_set()
            dialog.transient(self)

            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(padx=20, pady=20, fill="both", expand=True)

            warning_label = ctk.CTkLabel(
                main_frame,
                text="⚠️",
                font=("Segoe UI", 36),
                text_color=ProfessionalTheme.COLORS["warning"],
            )
            warning_label.pack(pady=(10, 5))

            message_label = ctk.CTkLabel(
                main_frame,
                text="There are downloads in progress. Are you sure you want to exit?",
                font=("Segoe UI", 12),
                wraplength=350,
                justify="center",
            )
            message_label.pack(pady=15, padx=10)

            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=10)

            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="Cancel",
                command=dialog.destroy,
                width=120,
                height=32,
                fg_color=ProfessionalTheme.COLORS["foreground"],
                hover_color="#333345",
            )
            cancel_btn.pack(side="left", padx=10, expand=True)

            confirm_btn = ctk.CTkButton(
                buttons_frame,
                text="Exit",
                command=lambda: (dialog.destroy(), self.destroy()),
                width=120,
                height=32,
                fg_color=ProfessionalTheme.COLORS["warning"],
                hover_color="#D69A57",
            )
            confirm_btn.pack(side="right", padx=10, expand=True)

            WindowUtils.center(dialog)
        else:
            # If no downloads, close directly
            self.destroy()

    def destroy(self):
        """Overrides the destroy method to clean up resources"""
        # Additional cleanup can be added here if necessary
        super().destroy()
