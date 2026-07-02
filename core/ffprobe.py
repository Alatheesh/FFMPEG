import json
import subprocess


class FFProbe:

    def __init__(self, ffprobe: str = "ffprobe"):
        self.ffprobe = ffprobe

    def probe(self, file_path: str):

        command = [
            self.ffprobe,
            "-v", "quiet",
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
            raise RuntimeError(result.stderr)

        return json.loads(result.stdout)

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
