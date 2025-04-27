# YT_Audio_Downloader\src\models\download_observer.py
from abc import ABC, abstractmethod


class DownloadObserver(ABC):
    @abstractmethod
    def on_progress_update(self, task):
        pass

    @abstractmethod
    def on_task_complete(self, task):
        pass

    @abstractmethod
    def on_task_error(self, task):
        pass
