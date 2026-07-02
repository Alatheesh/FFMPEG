import json
import subprocess
from pathlib import Path


class FFProbe:

    def __init__(self, ffprobe: str = "ffprobe"):
        self.ffprobe = ffprobe

    def probe(self, file_path: str):

        file_path = str(Path(file_path))

        command = [
            self.ffprobe,
            "-hide_banner",
            "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            file_path
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"""
FFprobe execution failed.

File:
{file_path}

Command:
{' '.join(command)}

Return Code:
{result.returncode}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""
            )

        if not result.stdout.strip():
            raise RuntimeError(
                f"""
FFprobe returned no output.

File:
{file_path}
"""
            )

        try:
            return json.loads(result.stdout)

        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"""
Invalid JSON received from FFprobe.

File:
{file_path}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""
            ) from e

    @staticmethod
    def get_video_streams(info):
        return [
            s for s in info.get("streams", [])
            if s.get("codec_type") == "video"
        ]

    @staticmethod
    def get_audio_streams(info):
        return [
            s for s in info.get("streams", [])
            if s.get("codec_type") == "audio"
        ]

    @staticmethod
    def get_subtitle_streams(info):
        return [
            s for s in info.get("streams", [])
            if s.get("codec_type") == "subtitle"
        ]

    @staticmethod
    def get_attachment_streams(info):
        return [
            s for s in info.get("streams", [])
            if s.get("codec_type") == "attachment"
        ]

    @staticmethod
    def get_chapters(info):
        return info.get("chapters", [])
