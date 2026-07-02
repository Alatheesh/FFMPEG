from __future__ import annotations

from pathlib import Path


class FFmpegCommandBuilder:
    """
    FFmpeg Command Builder

    Responsible for building complete FFmpeg commands.

    Supports:
    - Multiple inputs
    - Stream mapping
    - Video/Audio filters
    - Codec selection
    - Metadata
    - Output options
    """

    def __init__(self):

        self.reset()

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.inputs=[]
        self.maps=[]

        self.arguments=[]

        self.video_filters=[]
        self.audio_filters=[]

        self.metadata=[]

        self.video_codec=None
        self.audio_codec=None
        self.subtitle_codec=None

        self.output=None

        self.overwrite=True

        return self

    # ==================================================
    # Inputs
    # ==================================================

    def add_input(
        self,
        file
    ):

        self.inputs.append(
            str(file)
        )

        return self

    def insert_input(
        self,
        index,
        file
    ):

        self.inputs.insert(
            index,
            str(file)
        )

        return self

    def remove_input(
        self,
        index
    ):

        del self.inputs[index]

        return self

    def clear_inputs(self):

        self.inputs.clear()

        return self

    # ==================================================
    # Maps
    # ==================================================

    def add_map(
        self,
        stream
    ):

        self.maps.append(
            str(stream)
        )

        return self

    def extend_maps(
        self,
        streams
    ):

        for stream in streams:

            self.maps.append(
                str(stream)
            )

        return self

    def clear_maps(self):

        self.maps.clear()

        return self

    # ==================================================
    # Generic Arguments
    # ==================================================

    def add_argument(
        self,
        *args
    ):

        for arg in args:

            self.arguments.append(
                str(arg)
            )

        return self

    def add_arguments(
        self,
        arguments
    ):

        for arg in arguments:

            self.arguments.append(
                str(arg)
            )

        return self

    # ==================================================
    # Filters
    # ==================================================

    def add_video_filter(
        self,
        filter_text
    ):

        self.video_filters.append(
            filter_text
        )

        return self

    def add_audio_filter(
        self,
        filter_text
    ):

        self.audio_filters.append(
            filter_text
        )

        return self

    def clear_filters(self):

        self.video_filters.clear()
        self.audio_filters.clear()

        return self
    # ==================================================
    # Codecs
    # ==================================================

    def set_video_codec(
        self,
        codec
    ):

        self.video_codec=str(codec)

        return self

    def set_audio_codec(
        self,
        codec
    ):

        self.audio_codec=str(codec)

        return self

    def set_subtitle_codec(
        self,
        codec
    ):

        self.subtitle_codec=str(codec)

        return self

    # ==================================================
    # Copy Helpers
    # ==================================================

    def copy_video(self):

        return self.set_video_codec(
            "copy"
        )

    def copy_audio(self):

        return self.set_audio_codec(
            "copy"
        )

    def copy_subtitle(self):

        return self.set_subtitle_codec(
            "copy"
        )

    def copy_all(self):

        self.copy_video()
        self.copy_audio()
        self.copy_subtitle()

        return self

    # ==================================================
    # Metadata
    # ==================================================

    def add_metadata(
        self,
        key,
        value
    ):

        self.metadata.append(
            (
                str(key),
                str(value)
            )
        )

        return self

    def add_stream_metadata(
        self,
        stream,
        index,
        key,
        value
    ):

        self.metadata.append(
            (
                f"{stream}:{index}:{key}",
                str(value)
            )
        )

        return self

    def clear_metadata(self):

        self.metadata.clear()

        return self

    # ==================================================
    # Output
    # ==================================================

    def set_output(
        self,
        file
    ):

        self.output=str(file)

        return self

    def enable_overwrite(
        self
    ):

        self.overwrite=True

        return self

    def disable_overwrite(
        self
    ):

        self.overwrite=False

        return self

    # ==================================================
    # Presets
    # ==================================================

    def set_crf(
        self,
        value
    ):

        self.add_argument(
            "-crf",
            value
        )

        return self

    def set_preset(
        self,
        preset
    ):

        self.add_argument(
            "-preset",
            preset
        )

        return self

    def set_video_bitrate(
        self,
        bitrate
    ):

        self.add_argument(
            "-b:v",
            bitrate
        )

        return self

    def set_audio_bitrate(
        self,
        bitrate
    ):

        self.add_argument(
            "-b:a",
            bitrate
        )

        return self

    # ==================================================
    # Misc
    # ==================================================

    def hide_banner(self):

        self.add_argument(
            "-hide_banner"
        )

        return self

    def loglevel(
        self,
        level="error"
    ):

        self.add_argument(
            "-loglevel",
            level
        )

        return self

    def shortest(self):

        self.add_argument(
            "-shortest"
        )

        return self

    def faststart(self):

        self.add_argument(
            "-movflags",
            "+faststart"
        )

        return self
    # ==================================================
    # Filter Assembly
    # ==================================================

    def build_video_filters(self):

        if not self.video_filters:
            return []

        return [
            "-vf",
            ",".join(self.video_filters)
        ]

    def build_audio_filters(self):

        if not self.audio_filters:
            return []

        return [
            "-af",
            ",".join(self.audio_filters)
        ]

    def add_complex_filter(
        self,
        filter_text
    ):

        self.add_argument(
            "-filter_complex",
            filter_text
        )

        return self

    # ==================================================
    # Build Sections
    # ==================================================

    def build_inputs(self):

        command=[]

        for file in self.inputs:

            command.extend([
                "-i",
                file
            ])

        return command

    def build_maps(self):

        command=[]

        for stream in self.maps:

            command.extend([
                "-map",
                stream
            ])

        return command

    def build_codecs(self):

        command=[]

        if self.video_codec:

            command.extend([
                "-c:v",
                self.video_codec
            ])

        if self.audio_codec:

            command.extend([
                "-c:a",
                self.audio_codec
            ])

        if self.subtitle_codec:

            command.extend([
                "-c:s",
                self.subtitle_codec
            ])

        return command

    def build_metadata(self):

        command=[]

        for key,value in self.metadata:

            if ":" in key:

                parts=key.split(":")

                stream=parts[0]
                index=parts[1]
                tag=":".join(parts[2:])

                command.extend([
                    f"-metadata:s:{stream}:{index}",
                    f"{tag}={value}"
                ])

            else:

                command.extend([
                    "-metadata",
                    f"{key}={value}"
                ])

        return command

    # ==================================================
    # Validation
    # ==================================================

    def validate(self):

        if not self.inputs:
            raise ValueError(
                "No input files specified."
            )

        if self.output is None:
            raise ValueError(
                "Output file not specified."
            )

        return True

    # ==================================================
    # Preview
    # ==================================================

    def preview(self):

        return " ".join(
            self.build()
        )
    # ==================================================
    # Build
    # ==================================================

    def build(self):

        self.validate()

        command=["ffmpeg"]

        if self.overwrite:
            command.append("-y")
        else:
            command.append("-n")

        command.extend(self.arguments)

        command.extend(
            self.build_inputs()
        )

        command.extend(
            self.build_maps()
        )

        command.extend(
            self.build_video_filters()
        )

        command.extend(
            self.build_audio_filters()
        )

        command.extend(
            self.build_codecs()
        )

        command.extend(
            self.build_metadata()
        )

        command.append(
            self.output
        )

        return command

    # ==================================================
    # Serialization
    # ==================================================

    def to_dict(self):

        return {
            "inputs":list(self.inputs),
            "maps":list(self.maps),
            "arguments":list(self.arguments),
            "video_filters":list(self.video_filters),
            "audio_filters":list(self.audio_filters),
            "metadata":list(self.metadata),
            "video_codec":self.video_codec,
            "audio_codec":self.audio_codec,
            "subtitle_codec":self.subtitle_codec,
            "output":self.output,
            "overwrite":self.overwrite
        }

    @classmethod
    def from_dict(
        cls,
        data
    ):

        builder=cls()

        builder.inputs=data.get(
            "inputs",
            []
        )

        builder.maps=data.get(
            "maps",
            []
        )

        builder.arguments=data.get(
            "arguments",
            []
        )

        builder.video_filters=data.get(
            "video_filters",
            []
        )

        builder.audio_filters=data.get(
            "audio_filters",
            []
        )

        builder.metadata=data.get(
            "metadata",
            []
        )

        builder.video_codec=data.get(
            "video_codec"
        )

        builder.audio_codec=data.get(
            "audio_codec"
        )

        builder.subtitle_codec=data.get(
            "subtitle_codec"
        )

        builder.output=data.get(
            "output"
        )

        builder.overwrite=data.get(
            "overwrite",
            True
        )

        return builder

    # ==================================================
    # Information
    # ==================================================

    def command_string(self):

        return " ".join(
            self.build()
        )

    def input_count(self):

        return len(
            self.inputs
        )

    def map_count(self):

        return len(
            self.maps
        )

    # ==================================================
    # Magic Methods
    # ==================================================

    def __len__(self):

        return len(
            self.build()
        )

    def __iter__(self):

        return iter(
            self.build()
        )

    def __repr__(self):

        return (
            "<FFmpegCommandBuilder "
            f"inputs={len(self.inputs)} "
            f"maps={len(self.maps)} "
            f"output={self.output}>"
        )
