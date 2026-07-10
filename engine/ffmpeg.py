import asyncio
import logging
import re
import shutil
import os
from engine.models import Workspace

logger = logging.getLogger(__name__)

def compile_ffmpeg_command(workspace: Workspace, output_path: str) -> list:
    """
    Compiles the workspace pipeline operations into a single FFmpeg command.
    Returns a list of CLI arguments.
    """
    ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
    
    # Target files
    main_video = workspace.assets[workspace.main_video_id]
    main_video_path = main_video.file_path
    
    # Trace inputs
    inputs = [main_video_path]  # Input index 0 is always main video
    
    # Initialize track inventories based on main video metadata
    main_meta = main_video.metadata
    
    audio_tracks = []
    for t in main_meta.get("audio_tracks", []):
        audio_tracks.append({
            "input_idx": 0,
            "stream_idx": len(audio_tracks), # stream index inside its input
            "codec": t.get("codec", "copy"),
            "title": t.get("title", f"Track {len(audio_tracks)+1}"),
            "language": t.get("language", "und"),
            "default": t.get("default", False),
            "forced": t.get("forced", False)
        })
        
    sub_tracks = []
    for t in main_meta.get("subtitle_tracks", []):
        sub_tracks.append({
            "input_idx": 0,
            "stream_idx": len(sub_tracks),
            "codec": t.get("codec", "copy"),
            "title": t.get("title", f"Subtitle {len(sub_tracks)+1}"),
            "language": t.get("language", "und"),
            "default": t.get("default", False),
            "forced": t.get("forced", False)
        })
        
    video_tracks = [{
        "input_idx": 0,
        "stream_idx": 0,
        "codec": "copy",
        "disposition": "default"
    }]
    
    global_metadata = {}
    trim_params = None
    compression_params = None
    burn_subtitle_idx = None
    
    # Evaluate Pipeline
    for op in workspace.pipeline:
        op_type = op.op_type
        params = op.params
        
        if op_type == "replace_audio":
            asset_id = params.get("asset_id")
            track_idx = params.get("track_index") # index in the output track list
            if asset_id in workspace.assets:
                asset = workspace.assets[asset_id]
                inputs.append(asset.file_path)
                new_input_idx = len(inputs) - 1
                
                # Replace the track in audio_tracks
                if 0 <= track_idx < len(audio_tracks):
                    audio_tracks[track_idx] = {
                        "input_idx": new_input_idx,
                        "stream_idx": 0,
                        "codec": "copy",
                        "title": params.get("title", "Replaced Audio"),
                        "language": params.get("language", "und"),
                        "default": params.get("default", True),
                        "forced": False
                    }
                    
        elif op_type == "remove_audio":
            track_idx = params.get("track_index")
            if 0 <= track_idx < len(audio_tracks):
                audio_tracks.pop(track_idx)
                
        elif op_type == "rename_audio":
            track_idx = params.get("track_index")
            if 0 <= track_idx < len(audio_tracks):
                audio_tracks[track_idx]["title"] = params.get("title", audio_tracks[track_idx]["title"])
                audio_tracks[track_idx]["language"] = params.get("language", audio_tracks[track_idx]["language"])
                
        elif op_type == "set_audio_default":
            track_idx = params.get("track_index")
            for i, t in enumerate(audio_tracks):
                t["default"] = (i == track_idx)
                
        elif op_type == "add_audio":
            asset_id = params.get("asset_id")
            if asset_id in workspace.assets:
                asset = workspace.assets[asset_id]
                inputs.append(asset.file_path)
                new_input_idx = len(inputs) - 1
                audio_tracks.append({
                    "input_idx": new_input_idx,
                    "stream_idx": 0,
                    "codec": "copy",
                    "title": params.get("title", f"Added Audio {len(audio_tracks)+1}"),
                    "language": params.get("language", "und"),
                    "default": params.get("default", False),
                    "forced": False
                })
                
        elif op_type == "add_subtitle":
            asset_id = params.get("asset_id")
            if asset_id in workspace.assets:
                asset = workspace.assets[asset_id]
                inputs.append(asset.file_path)
                new_input_idx = len(inputs) - 1
                sub_tracks.append({
                    "input_idx": new_input_idx,
                    "stream_idx": 0,
                    "codec": "srt" if asset.file_path.endswith(".srt") else "ass" if asset.file_path.endswith(".ass") else "copy",
                    "title": params.get("title", f"Subtitle {len(sub_tracks)+1}"),
                    "language": params.get("language", "und"),
                    "default": params.get("default", False),
                    "forced": False
                })
                
        elif op_type == "remove_subtitle":
            track_idx = params.get("track_index")
            if 0 <= track_idx < len(sub_tracks):
                sub_tracks.pop(track_idx)
                
        elif op_type == "rename_subtitle":
            track_idx = params.get("track_index")
            if 0 <= track_idx < len(sub_tracks):
                sub_tracks[track_idx]["title"] = params.get("title", sub_tracks[track_idx]["title"])
                sub_tracks[track_idx]["language"] = params.get("language", sub_tracks[track_idx]["language"])
                
        elif op_type == "burn_subtitle":
            # For burning subtitles directly into video frames (requires encoding)
            track_idx = params.get("track_index")
            burn_subtitle_idx = track_idx
            
        elif op_type == "add_thumbnail":
            asset_id = params.get("asset_id")
            if asset_id in workspace.assets:
                asset = workspace.assets[asset_id]
                inputs.append(asset.file_path)
                new_input_idx = len(inputs) - 1
                # In MKV/MP4 we can map the cover image as an attached picture or video stream
                video_tracks.append({
                    "input_idx": new_input_idx,
                    "stream_idx": 0,
                    "codec": "copy",
                    "disposition": "attached_pic"
                })
                
        elif op_type == "set_metadata":
            global_metadata.update(params)
            
        elif op_type == "trim_video":
            trim_params = params  # {"start": float, "end": float}
            
        elif op_type == "compress_video":
            compression_params = params  # {"preset": str}

    # Start constructing FFmpeg Command
    cmd = [ffmpeg_path, "-y"]
    
    # 1. Inputs
    for inp in inputs:
        cmd.extend(["-i", inp])
        
    # 2. Mappings & Codecs
    # Video
    cmd.extend(["-map", f"{video_tracks[0]['input_idx']}:v:{video_tracks[0]['stream_idx']}"])
    
    # Check if re-encoding is forced (due to compression, trim, or subtitle burn-in)
    video_codec = workspace.output_settings.get("video_codec", "copy")
    filter_complex = []
    
    if burn_subtitle_idx is not None and 0 <= burn_subtitle_idx < len(sub_tracks):
        # To burn subtitles, we must transcode and use video filter
        # Get subtitle path
        sub_track = sub_tracks[burn_subtitle_idx]
        sub_path = inputs[sub_track["input_idx"]]
        # Escape path for FFmpeg filter block
        safe_path = sub_path.replace(":", "\\:").replace("\\", "/")
        
        # Build filter argument depending on file extension
        if safe_path.endswith(".srt"):
            filter_complex.append(f"subtitles='{safe_path}'")
        else:
            filter_complex.append(f"ass='{safe_path}'")
            
        video_codec = "libx264"  # Force transcoding to burn subtitles
        # Since it is burned in, remove the track from text attachments list
        sub_tracks.pop(burn_subtitle_idx)
        
    if compression_params:
        video_codec = "libx264"
        preset = compression_params.get("preset", "medium")
        cmd.extend(["-c:v", video_codec, "-crf", "23", "-preset", preset])
    elif video_codec == "libx264":
        cmd.extend(["-c:v", "libx264", "-preset", "medium"])
    else:
        cmd.extend(["-c:v", "copy"])
        
    if filter_complex:
        cmd.extend(["-vf", ",".join(filter_complex)])
        
    # Audio Mappings
    audio_codec = workspace.output_settings.get("audio_codec", "copy")
    for i, t in enumerate(audio_tracks):
        cmd.extend(["-map", f"{t['input_idx']}:a:{t['stream_idx']}"])
        # Codecs
        cmd.extend([f"-c:a:{i}", audio_codec])
        # Metadata
        cmd.extend([f"-metadata:s:a:{i}", f"title={t['title']}"])
        cmd.extend([f"-metadata:s:a:{i}", f"language={t['language']}"])
        # Dispositions
        cmd.extend([f"-disposition:a:{i}", "default" if t["default"] else "0"])
        
    # Subtitle Mappings
    for i, t in enumerate(sub_tracks):
        cmd.extend(["-map", f"{t['input_idx']}:s:{t['stream_idx']}"])
        
        # Determine subtitle codec (mkv allows srt/ass copy, mp4 requires conversion/mov_text)
        sub_out_codec = "copy"
        if workspace.output_settings.get("format") == "mp4":
            sub_out_codec = "mov_text"
        elif t["codec"] == "srt":
            sub_out_codec = "srt"
        elif t["codec"] == "ass":
            sub_out_codec = "ass"
            
        cmd.extend([f"-c:s:{i}", sub_out_codec])
        cmd.extend([f"-metadata:s:s:{i}", f"title={t['title']}"])
        cmd.extend([f"-metadata:s:s:{i}", f"language={t['language']}"])
        cmd.extend([f"-disposition:s:{i}", "default" if t["default"] else "0"])

    # Thumbnail / Cover mappings (if present)
    for i in range(1, len(video_tracks)):
        vt = video_tracks[i]
        cmd.extend(["-map", f"{vt['input_idx']}:v:{vt['stream_idx']}"])
        cmd.extend([f"-c:v:{i}", "copy"])
        cmd.extend([f"-disposition:v:{i}", "attached_pic"])

    # 3. Trim seeks
    if trim_params:
        # Seeking on output side ensures precision
        start = trim_params.get("start", 0.0)
        end = trim_params.get("end", 0.0)
        cmd.extend(["-ss", str(start)])
        if end > start:
            cmd.extend(["-to", str(end)])

    # 4. Global Metadata
    for k, v in global_metadata.items():
        cmd.extend(["-metadata", f"{k}={v}"])

    # Output file
    cmd.append(output_path)
    return cmd

async def execute_ffmpeg(cmd: list, duration: float, progress_callback=None) -> bool:
    """
    Executes FFmpeg asynchronously and parses stdout/stderr to feed the progress callback.
    """
    logger.info(f"Executing FFmpeg: {' '.join(cmd)}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Pattern to extract time progress: time=00:00:05.12
        time_pattern = re.compile(r"time=(\d+):(\d+):(\d+)\.(\d+)")
        
        # Read stderr line-by-line (FFmpeg reports progress in stderr)
        while True:
            line_bytes = await process.stderr.readline()
            if not line_bytes:
                break
            
            line = line_bytes.decode("utf-8", errors="ignore")
            match = time_pattern.search(line)
            if match and duration > 0 and progress_callback:
                hours, minutes, seconds, hundredths = map(int, match.groups())
                current_time = hours * 3600 + minutes * 60 + seconds + hundredths / 100.0
                percent = min(100, int((current_time / duration) * 100))
                await progress_callback(percent)
                
        await process.wait()
        return process.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg execution failed: {e}")
        return False
