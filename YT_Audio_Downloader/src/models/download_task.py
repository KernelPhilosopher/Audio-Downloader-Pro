"""
Download Task Model

Represents a single download task with its properties and status information.

Attributes:
    url (str): The YouTube URL to download from
    output_format (str): The desired audio output format
    progress (float): Download progress percentage
    status (str): Current status of the download
    error (str): Error message if any occurred
"""

from dataclasses import dataclass


@dataclass
class DownloadTask:
    url: str
    output_format: str
    progress: float = 0.0
    status: str = "Pending"
    error: str = None
