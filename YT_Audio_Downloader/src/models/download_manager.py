"""
Download Manager Module

This module provides the core functionality for managing YouTube audio downloads.
It implements a multi-threaded download system with progress tracking and observer notifications.
"""

from pathlib import Path
import queue
import threading
import yt_dlp
from typing import List
from . import DownloadObserver


class DownloadManager:
    """
    Manages concurrent YouTube audio downloads using a thread pool architecture.

    Features:
    - Multi-threaded download processing
    - Progress tracking and reporting
    - Observer pattern for status updates
    - Configurable output directory
    - Error handling and recovery
    """

    def __init__(self, output_directory: Path, max_workers: int = 3):
        """
        Initializes the download manager with specified configuration.

        Args:
            output_directory (Path): Target directory for downloaded files
            max_workers (int): Maximum number of concurrent download threads
        """
        self.output_directory = output_directory
        self.task_queue = queue.Queue()
        self.observers: List[DownloadObserver] = []
        self.workers = []
        self.is_running = False
        self._init_workers(max_workers)

    def _init_workers(self, max_workers: int):
        """
        Initializes the worker thread pool.

        Args:
            max_workers (int): Number of worker threads to create

        Creates daemon threads that process downloads concurrently.
        """
        for _ in range(max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)

    def register_observer(self, observer: DownloadObserver):
        """
        Registers an observer to receive updates about task progress, completion, or errors.

        Args:
            observer (DownloadObserver): The observer to register.
        """
        self.observers.append(observer)

    def enqueue_task(self, task):
        """
        Adds a new download task to the queue.

        Args:
            task: The task object containing download details (e.g., URL, output format).
        """
        self.task_queue.put(task)

    def start_processing(self):
        """
        Starts processing tasks in the queue by setting the running flag to True.
        """
        self.is_running = True

    def _worker_loop(self):
        """
        Worker thread loop that processes tasks from the queue.
        """
        while True:
            task = self.task_queue.get()  # Get the next task from the queue
            if not self.is_running:
                break  # Exit the loop if the manager is no longer running
            try:
                self._process_download(task)  # Process the download task
            except Exception as e:
                self._notify_error(task, str(e))  # Notify observers of any errors
            finally:
                self.task_queue.task_done()  # Mark the task as done

    def _process_download(self, task):
        """
        Processes a single download task using yt_dlp.

        Args:
            task: The task object containing download details.
        """
        task.status = "Downloading"  # Update task status to "Downloading"
        ydl_opts = self._build_ydl_options(task)  # Build yt_dlp options for the task

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(
                    task.url, download=True
                )  # Extract and download the video/audio
                if not info:
                    raise Exception(
                        "Content not available"
                    )  # Raise an error if no info is returned
            self._notify_completion(task)  # Notify observers of task completion
        except Exception as e:
            self._notify_error(task, str(e))  # Notify observers of any errors

    def _build_ydl_options(self, task):
        """
        Builds the yt_dlp options for the given task.

        Args:
            task: The task object containing download details.

        Returns:
            dict: A dictionary of yt_dlp options.
        """
        return {
            "format": "bestaudio/best",  # Download the best available audio format
            "outtmpl": str(
                self.output_directory / "%(title)s_[%(id)s].%(ext)s"
            ),  # Output file template
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",  # Extract audio using FFmpeg
                    "preferredcodec": task.output_format,  # Set the preferred audio codec
                    "preferredquality": "192",  # Set the preferred audio quality
                }
            ],
            "progress_hooks": [
                lambda d: self._handle_progress(task, d)
            ],  # Hook to handle progress updates
            "quiet": True,  # Suppress yt_dlp output
            "noplaylist": True,  # Disable playlist downloads
            "extractor_args": {
                "youtube": {"formats": "missing_pot"}
            },  # Additional extractor arguments
        }

    def _handle_progress(self, task, progress_data):
        """
        Handles progress updates from yt_dlp and notifies observers.

        Args:
            task: The task object being downloaded.
            progress_data (dict): Progress data from yt_dlp.
        """
        if progress_data["status"] == "downloading":
            try:
                downloaded = progress_data.get(
                    "downloaded_bytes", 0
                )  # Bytes downloaded so far
                total = progress_data.get("total_bytes") or progress_data.get(
                    "total_bytes_estimate", 1
                )  # Total bytes to download
                task.progress = min(
                    99.9, (downloaded / total) * 100
                )  # Calculate progress percentage
            except Exception:
                task.progress = 0.0  # Set progress to 0 if an error occurs
            self._notify_progress(task)  # Notify observers of progress updates

    def _notify_progress(self, task):
        """
        Notifies all registered observers about task progress updates.

        Args:
            task: The task object being updated.
        """
        for observer in self.observers:
            observer.on_progress_update(task)

    def _notify_completion(self, task):
        """
        Notifies all registered observers about task completion.

        Args:
            task: The task object that has been completed.
        """
        task.status = "Completed"  # Update task status to "Completed"
        task.progress = 100.0  # Set progress to 100%
        for observer in self.observers:
            observer.on_task_complete(task)

    def _notify_error(self, task, error):
        """
        Notifies all registered observers about a task error.

        Args:
            task: The task object that encountered an error.
            error (str): The error message.
        """
        task.status = "Error"  # Update task status to "Error"
        task.error = error  # Set the error message
        for observer in self.observers:
            observer.on_task_error(task)
