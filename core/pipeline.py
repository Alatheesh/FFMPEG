import os
from typing import List
from core.workspace import Workspace, Operation

class FFmpegCompiler:
    @staticmethod
    def compile(workspace: Workspace, output_dir: str) -> List[str]:
        """
        Translates structural pipeline queues directly into safe FFmpeg list flags.
        Does not execute commands natively.
        """
        # Find primary source video asset
        main_video = next((a for a in workspace.assets.values() if a.asset_type == 'video'), None)
        if not main_video:
            raise ValueError("No primary video asset found in workspace pipeline.")

        input_files = [main_video.file_path]
        ffmpeg_args = ["ffmpeg", "-y"]
        
        # Build list of maps and metadata modifiers
        metadata_map: List[str] = []
        audio_replaced = False
        
        for op in workspace.pipeline:
            if op.action == "set_title":
                title_val = op.parameters.get("title", "")
                metadata_map.extend(["-metadata", f"title={title_val}"])
                
            elif op.action == "replace_audio":
                audio_asset_id = op.parameters.get("asset_id")
                audio_asset = workspace.assets.get(audio_asset_id)
                if audio_asset:
                    input_files.append(audio_asset.file_path)
                    audio_replaced = True

        # Append inputs
        for infile in input_files:
            ffmpeg_args.extend(["-i", infile])

        # Map streams based on operational pipeline decisions
        if audio_replaced:
            # Map video from 1st input, audio from 2nd input
            ffmpeg_args.extend(["-map", "0:v:0", "-map", "1:a:0"])
        else:
            # Mirror stream topology
            ffmpeg_args.extend(["-map", "0"])

        # Default fallback to stream copy (Non-destructive optimization)
        ffmpeg_args.extend(["-c", "copy"])
        ffmpeg_args.extend(metadata_map)

        output_filename = f"out_{workspace.user_id}.{workspace.output_format}"
        output_path = os.path.join(output_dir, output_filename)
        ffmpeg_args.append(output_path)
        
        return ffmpeg_args
