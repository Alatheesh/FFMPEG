from pathlib import Path

from core.command_builder import FFmpegCommandBuilder
from core.ffmpeg import FFmpeg
from constants import Operation


class PipelineProcessor:

    def __init__(self, workspace):

        self.workspace = workspace

    # ----------------------------------------------------
    # Execute Pipeline
    # ----------------------------------------------------

    def execute(self):

        video = self.workspace.get_main_video()

        if not video:
            raise ValueError("No video selected.")

        current_file = video.path

        for step in self.workspace.pipeline.pending():

            operation = step.operation

            if operation == Operation.REMOVE_AUDIO.value:

                current_file = self.remove_audio(
                    current_file,
                    step
                )

                step.status = "completed"

            else:

                step.status = "failed"

                step.error = (
                    f"{operation} is not implemented yet."
                )

        return current_file

    # ----------------------------------------------------
    # Remove Audio
    # ----------------------------------------------------

    def remove_audio(
        self,
        input_file,
        step
    ):

        output_file = str(
            Path(input_file).with_name(
                Path(input_file).stem +
                "_edited.mkv"
            )
        )

        builder = FFmpegCommandBuilder()

        builder.add_input(input_file)

        # Copy video
        builder.add_map("0:v")

        # Copy subtitles if any
        builder.add_map("0:s?")

        # Copy attachments
        builder.add_map("0:t?")

        # Copy chapters
        builder.add_argument("-map_chapters", "0")

        builder.copy_all()

        builder.set_output(output_file)

        command = builder.build()

        success, log = FFmpeg.run(command)

        if not success:
            raise RuntimeError(log)

        return output_file
