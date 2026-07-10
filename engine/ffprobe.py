import asyncio
import json
import logging
import shutil

logger = logging.getLogger(__name__)

async def run_ffprobe(file_path: str) -> dict:
    """
    Runs ffprobe asynchronously on the target file and parses format/stream details to JSON.
    """
    ffprobe_path = shutil.which("ffprobe")
    if not ffprobe_path:
        logger.error("ffprobe executable not found in PATH!")
        return {}

    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"ffprobe returned non-zero exit code: {process.returncode}. Stderr: {stderr.decode()}")
            return {}
            
        data = json.loads(stdout.decode("utf-8"))
        return parse_ffprobe_metadata(data)
    except Exception as e:
        logger.error(f"Failed to run ffprobe on {file_path}: {e}")
        return {}

def parse_ffprobe_metadata(probe_data: dict) -> dict:
    """
    Parses and cleans the raw JSON response from ffprobe.
    """
    streams = probe_data.get("streams", [])
    format_info = probe_data.get("format", {})
    
    parsed = {
        "duration": float(format_info.get("duration", 0.0)),
        "size": int(format_info.get("size", 0)),
        "bitrate": int(format_info.get("bit_rate", 0)) if format_info.get("bit_rate") else 0,
        "format_name": format_info.get("format_name", ""),
        "video_tracks": [],
        "audio_tracks": [],
        "subtitle_tracks": [],
        "attachments": []
    }
    
    for stream in streams:
        codec_type = stream.get("codec_type")
        codec_name = stream.get("codec_name", "")
        index = stream.get("index")
        
        tags = stream.get("tags", {})
        language = tags.get("language", "und")
        title = tags.get("title", f"Track {index}")
        
        disposition = stream.get("disposition", {})
        is_default = bool(disposition.get("default", 0))
        is_forced = bool(disposition.get("forced", 0))
        
        track_info = {
            "index": index,
            "codec": codec_name,
            "title": title,
            "language": language,
            "default": is_default,
            "forced": is_forced
        }
        
        if codec_type == "video":
            # Add resolution metrics
            track_info["width"] = stream.get("width")
            track_info["height"] = stream.get("height")
            track_info["pix_fmt"] = stream.get("pix_fmt")
            parsed["video_tracks"].append(track_info)
            
        elif codec_type == "audio":
            track_info["channels"] = stream.get("channels")
            track_info["sample_rate"] = int(stream.get("sample_rate", 0)) if stream.get("sample_rate") else 0
            parsed["audio_tracks"].append(track_info)
            
        elif codec_type == "subtitle":
            parsed["subtitle_tracks"].append(track_info)
            
        elif codec_type == "attachment":
            parsed["attachments"].append({
                "index": index,
                "filename": tags.get("filename", "unknown"),
                "mimetype": tags.get("mimetype", "unknown")
            })
            
    return parsed
