import json
import subprocess


def probe(file_path: str):
    """
    Read media information using FFprobe.
    Returns the complete JSON output.
    """

    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return json.loads(result.stdout)


def get_video_streams(info):
    return [
        s for s in info["streams"]
        if s["codec_type"] == "video"
    ]


def get_audio_streams(info):
    return [
        s for s in info["streams"]
        if s["codec_type"] == "audio"
    ]


def get_subtitle_streams(info):
    return [
        s for s in info["streams"]
        if s["codec_type"] == "subtitle"
    ]


def get_attachment_streams(info):
    return [
        s for s in info["streams"]
        if s["codec_type"] == "attachment"
    ]


def get_chapter_streams(info):
    return info.get("chapters", [])
