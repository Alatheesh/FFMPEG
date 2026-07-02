from typing import List


class FFmpegCommandBuilder:

    def __init__(self):

        self.command = [
            "ffmpeg",
            "-y"
        ]

        self.inputs = []

        self.maps = []

        self.codecs = []

        self.metadata = []

        self.extra = []

        self.output = None

    # --------------------------
    # INPUTS
    # --------------------------

    def add_input(self, file):

        self.inputs.append(file)

    # --------------------------
    # MAPS
    # --------------------------

    def add_map(self, stream):

        self.maps.append(stream)

    # --------------------------
    # CODECS
    # --------------------------

    def copy_all(self):

        self.codecs.append([
            "-c",
            "copy"
        ])

    def set_video_codec(self, codec):

        self.codecs.append([
            "-c:v",
            codec
        ])

    def set_audio_codec(self, codec):

        self.codecs.append([
            "-c:a",
            codec
        ])

    def set_subtitle_codec(self, codec):

        self.codecs.append([
            "-c:s",
            codec
        ])

    # --------------------------
    # METADATA
    # --------------------------

    def add_metadata(self, key, value):

        self.metadata.append([
            "-metadata",
            f"{key}={value}"
        ])

    # --------------------------
    # EXTRA
    # --------------------------

    def add_argument(self, *args):

        self.extra.append(list(args))

    # --------------------------
    # OUTPUT
    # --------------------------

    def set_output(self, output):

        self.output = output

    # --------------------------
    # BUILD
    # --------------------------

    def build(self):

        cmd = self.command.copy()

        # Inputs

        for file in self.inputs:

            cmd.extend([
                "-i",
                file
            ])

        # Maps

        for stream in self.maps:

            cmd.extend([
                "-map",
                stream
            ])

        # Codecs

        for codec in self.codecs:

            cmd.extend(codec)

        # Metadata

        for meta in self.metadata:

            cmd.extend(meta)

        # Extra Arguments

        for arg in self.extra:

            cmd.extend(arg)

        # Output

        cmd.append(self.output)

        return cmd
