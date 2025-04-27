"""
Main controller module for the YouTube Audio Downloader application.

This module orchestrates the entire application flow by:
- Coordinating communication between views and models
- Managing the download process lifecycle
- Handling user interactions and input validation
- Ensuring dependency requirements are met
"""

from utils import WindowUtils
from models import DownloadManager
from models import DownloadTask
from views import MainView
from services import FFmpegService


class AppController:
    """
    Main application controller that coordinates the interaction between UI and business logic.

    Responsibilities:
    - Initializes and connects view and model components
    - Validates system dependencies
    - Manages download task creation and execution
    - Handles legal compliance checks
    """

    LEGAL_DISCLAIMER = "Software for legal use only. Download authorized content only."

    def __init__(self):
        """
        Initializes the application controller with required components.

        Sets up:
        - Download path configuration
        - Model initialization (DownloadManager)
        - View initialization (MainView)
        - Observer pattern configuration
        - System dependency verification
        """
        downloads_path = WindowUtils.get_downloads_path()
        self.model = DownloadManager(output_directory=downloads_path)
        self.view = MainView(self)
        self._setup_observers()
        self._verify_dependencies()

    def _setup_observers(self):
        """
        Configures the observer pattern implementation.

        Registers the view as an observer of the model to receive download status updates.
        This enables real-time UI updates based on download progress.
        """
        self.model.register_observer(self.view)

    def _verify_dependencies(self):
        """
        Verifies all required external dependencies.

        Currently checks:
        - FFmpeg availability

        Terminates the application if critical dependencies are missing.
        """
        if not FFmpegService.check_availability():
            self.view.show_error(
                "FFmpeg is not installed. Please install FFmpeg to use this application."
            )
            self.view.destroy()

    def start_downloads(self):
        """
        Initiates the download process workflow.

        Process:
        1. Validates legal compliance
        2. Processes provided URLs
        3. Creates and queues download tasks

        The actual downloads are handled asynchronously by the DownloadManager.
        """
        if not self._validate_legal():
            return
        self._process_urls()

    def _validate_legal(self) -> bool:
        """
        Validates user acceptance of legal requirements.

        Returns:
            bool: True if legal requirements are accepted, False otherwise.

        Shows a warning dialog if legal terms haven't been accepted.
        """
        if not self.view.legal_accepted():
            self.view.show_warning("Legal Warning", self.LEGAL_DISCLAIMER)
            return False
        return True

    def _process_urls(self):
        """
        Processes user-provided URLs and creates corresponding download tasks.

        - Validates URL presence
        - Creates DownloadTask instances for each URL
        - Enqueues tasks in the DownloadManager
        - Shows error if no URLs are provided
        """
        urls = self.view.get_urls()
        if not urls:
            self.view.show_error(
                "No URLs provided. Please enter at least one YouTube URL."
            )
            return

        for url in urls:
            task = DownloadTask(url=url.strip(), output_format=self.view.get_format())
            self.model.enqueue_task(task)

    def run(self):
        """
        Launches the application.

        - Starts the download processing system
        - Initializes and runs the main UI loop
        """
        self.model.start_processing()
        self.view.mainloop()
