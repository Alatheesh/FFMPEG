from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Dict,List,Optional

from constants import Operation
from core.ffmpeg import FFmpeg
from core.command_builder import FFmpegCommandBuilder
from core.stream_mapper import StreamMapper


class MediaEngine:

    """
    Executes queued operations.

    Managers create operations.

    MediaEngine executes them.
    """

    def __init__(self,workspace):

        self.workspace=workspace
        self.ffmpeg=FFmpeg()

    # ==================================================
    # Public
    # ==================================================

    async def process_audio(
        self,
        operations:List[Dict]
    ):

        return await self.process(
            operations
        )

    async def process_media(
        self,
        operations:List[Dict]
    ):

        return await self.process(
            operations
        )

    async def process(
        self,
        operations:List[Dict]
    ):

        video=self.workspace.get_main_video()

        if video is None:
            raise RuntimeError(
                "No video loaded."
            )

        current_file=video.path

        for operation in operations:

            current_file=await self.execute(
                current_file,
                operation
            )

        return current_file

    # ==================================================
    # Dispatcher
    # ==================================================

    async def execute(
        self,
        input_file:str,
        operation:Dict
    ):

        op=operation["operation"]
        data=operation["data"]

        if op==Operation.REMOVE_AUDIO.value:
            return await self.remove_audio(
                input_file,
                data
            )

        if op==Operation.REPLACE_AUDIO.value:
            return await self.replace_audio(
                input_file,
                data
            )

        if op==Operation.MERGE_AUDIO.value:
            return await self.merge_audio(
                input_file,
                data
            )

        if op==Operation.ADD_SUBTITLE.value:
            return await self.add_subtitle(
                input_file,
                data
            )

        if op==Operation.REMOVE_SUBTITLE.value:
            return await self.remove_subtitle(
                input_file,
                data
            )

        if op==Operation.REPLACE_SUBTITLE.value:
            return await self.replace_subtitle(
                input_file,
                data
            )

        if op==Operation.TRIM_VIDEO.value:
            return await self.trim_video(
                input_file,
                data
            )

        if op==Operation.CROP_VIDEO.value:
            return await self.crop_video(
                input_file,
                data
            )

        if op==Operation.RESIZE_VIDEO.value:
            return await self.resize_video(
                input_file,
                data
            )

        if op==Operation.ROTATE_VIDEO.value:
            return await self.rotate_video(
                input_file,
                data
            )

        if op==Operation.COMPRESS_VIDEO.value:
            return await self.compress_video(
                input_file,
                data
            )

        raise NotImplementedError(
            op
        )

    # ==================================================
    # Helpers
    # ==================================================

    def temp_output(
        self,
        input_file:str,
        suffix:str
    ):

        path=Path(input_file)

        return str(
            path.with_name(
                f"{path.stem}_{suffix}{path.suffix}"
            )
        )

    async def run(
        self,
        builder:FFmpegCommandBuilder
    ):

        command=builder.build()

        success,log=await asyncio.to_thread(
            self.ffmpeg.run,
            command
        )

        if not success:
            raise RuntimeError(log)

        return builder.output
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Dict,List,Optional

from constants import Operation
from core.ffmpeg import FFmpeg
from core.command_builder import FFmpegCommandBuilder
from core.stream_mapper import StreamMapper


class MediaEngine:

    """
    Executes queued operations.

    Managers create operations.

    MediaEngine executes them.
    """

    def __init__(self,workspace):

        self.workspace=workspace
        self.ffmpeg=FFmpeg()

    # ==================================================
    # Public
    # ==================================================

    async def process_audio(
        self,
        operations:List[Dict]
    ):

        return await self.process(
            operations
        )

    async def process_media(
        self,
        operations:List[Dict]
    ):

        return await self.process(
            operations
        )

    async def process(
        self,
        operations:List[Dict]
    ):

        video=self.workspace.get_main_video()

        if video is None:
            raise RuntimeError(
                "No video loaded."
            )

        current_file=video.path

        for operation in operations:

            current_file=await self.execute(
                current_file,
                operation
            )

        return current_file

    # ==================================================
    # Dispatcher
    # ==================================================

    async def execute(
        self,
        input_file:str,
        operation:Dict
    ):

        op=operation["operation"]
        data=operation["data"]

        if op==Operation.REMOVE_AUDIO.value:
            return await self.remove_audio(
                input_file,
                data
            )

        if op==Operation.REPLACE_AUDIO.value:
            return await self.replace_audio(
                input_file,
                data
            )

        if op==Operation.MERGE_AUDIO.value:
            return await self.merge_audio(
                input_file,
                data
            )

        if op==Operation.ADD_SUBTITLE.value:
            return await self.add_subtitle(
                input_file,
                data
            )

        if op==Operation.REMOVE_SUBTITLE.value:
            return await self.remove_subtitle(
                input_file,
                data
            )

        if op==Operation.REPLACE_SUBTITLE.value:
            return await self.replace_subtitle(
                input_file,
                data
            )

        if op==Operation.TRIM_VIDEO.value:
            return await self.trim_video(
                input_file,
                data
            )

        if op==Operation.CROP_VIDEO.value:
            return await self.crop_video(
                input_file,
                data
            )

        if op==Operation.RESIZE_VIDEO.value:
            return await self.resize_video(
                input_file,
                data
            )

        if op==Operation.ROTATE_VIDEO.value:
            return await self.rotate_video(
                input_file,
                data
            )

        if op==Operation.COMPRESS_VIDEO.value:
            return await self.compress_video(
                input_file,
                data
            )

        raise NotImplementedError(
            op
        )

    # ==================================================
    # Helpers
    # ==================================================

    def temp_output(
        self,
        input_file:str,
        suffix:str
    ):

        path=Path(input_file)

        return str(
            path.with_name(
                f"{path.stem}_{suffix}{path.suffix}"
            )
        )

    async def run(
        self,
        builder:FFmpegCommandBuilder
    ):

        command=builder.build()

        success,log=await asyncio.to_thread(
            self.ffmpeg.run,
            command
        )

        if not success:
            raise RuntimeError(log)

        return builder.output

    # ==================================================
    # Video
    # ==================================================

    async def trim_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "trim"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.add_argument("-ss",data["start"])
        builder.add_argument("-to",data["end"])
        builder.copy_all()
        builder.set_output(output)

        return await self.run(builder)

    async def crop_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "crop"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.add_video_filter(
            f"crop={data['width']}:{data['height']}:{data['x']}:{data['y']}"
        )

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def resize_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "resize"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.add_video_filter(
            f"scale={data['width']}:{data['height']}"
        )

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def rotate_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "rotate"
        )

        angle=data["angle"]

        if angle==90:
            vf="transpose=1"
        elif angle==180:
            vf="transpose=1,transpose=1"
        elif angle==270:
            vf="transpose=2"
        else:
            raise ValueError("Unsupported rotation.")

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.add_video_filter(vf)

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def compress_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "compress"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.set_video_codec(
            data.get(
                "video_codec",
                "libx264"
            )
        )

        builder.set_audio_codec(
            data.get(
                "audio_codec",
                "aac"
            )
        )

        builder.add_argument(
            "-crf",
            str(
                data.get(
                    "crf",
                    23
                )
            )
        )

        builder.add_argument(
            "-preset",
            data.get(
                "preset",
                "medium"
            )
        )

        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    # ==================================================
    # Container
    # ==================================================

    async def convert_container(
        self,
        input_file:str,
        data:Dict
    ):

        container=data["container"].lower()

        output=str(
            Path(input_file).with_suffix(
                "."+container
            )
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.copy_all()
        builder.set_output(output)

        return await self.run(builder)

    # ==================================================
    # Metadata
    # ==================================================

    async def update_metadata(
        self,
        input_file:str,
        metadata:Dict
    ):

        output=self.temp_output(
            input_file,
            "metadata"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.copy_all()

        for key,value in metadata.items():

            builder.add_argument(
                "-metadata",
                f"{key}={value}"
            )

        builder.set_output(output)

        return await self.run(builder)
    # ==================================================
    # Video
    # ==================================================

    async def trim_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "trim"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.add_argument("-ss",data["start"])
        builder.add_argument("-to",data["end"])
        builder.copy_all()
        builder.set_output(output)

        return await self.run(builder)

    async def crop_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "crop"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.add_video_filter(
            f"crop={data['width']}:{data['height']}:{data['x']}:{data['y']}"
        )

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def resize_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "resize"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.add_video_filter(
            f"scale={data['width']}:{data['height']}"
        )

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def rotate_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "rotate"
        )

        angle=data["angle"]

        if angle==90:
            vf="transpose=1"
        elif angle==180:
            vf="transpose=1,transpose=1"
        elif angle==270:
            vf="transpose=2"
        else:
            raise ValueError("Unsupported rotation.")

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.add_video_filter(vf)

        builder.copy_audio()
        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    async def compress_video(
        self,
        input_file:str,
        data:Dict
    ):

        output=self.temp_output(
            input_file,
            "compress"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.set_video_codec(
            data.get(
                "video_codec",
                "libx264"
            )
        )

        builder.set_audio_codec(
            data.get(
                "audio_codec",
                "aac"
            )
        )

        builder.add_argument(
            "-crf",
            str(
                data.get(
                    "crf",
                    23
                )
            )
        )

        builder.add_argument(
            "-preset",
            data.get(
                "preset",
                "medium"
            )
        )

        builder.copy_subtitle()

        builder.set_output(output)

        return await self.run(builder)

    # ==================================================
    # Container
    # ==================================================

    async def convert_container(
        self,
        input_file:str,
        data:Dict
    ):

        container=data["container"].lower()

        output=str(
            Path(input_file).with_suffix(
                "."+container
            )
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)
        builder.copy_all()
        builder.set_output(output)

        return await self.run(builder)

    # ==================================================
    # Metadata
    # ==================================================

    async def update_metadata(
        self,
        input_file:str,
        metadata:Dict
    ):

        output=self.temp_output(
            input_file,
            "metadata"
        )

        builder=FFmpegCommandBuilder()

        builder.add_input(input_file)

        builder.copy_all()

        for key,value in metadata.items():

            builder.add_argument(
                "-metadata",
                f"{key}={value}"
            )

        builder.set_output(output)

        return await self.run(builder)
