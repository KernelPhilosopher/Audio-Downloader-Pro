# YT_Audio_Downloader\src\services\ffmpeg_service.py
import subprocess


class FFmpegService:
    @staticmethod
    def check_availability():
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
