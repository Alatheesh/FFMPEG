from constants import Operation
from core.command_builder import FFmpegCommandBuilder
from core.ffmpeg import FFmpeg
from core.stream_mapper import StreamMapper


class OperationExecutor:
    """
    Executes a single pipeline operation.

    Input:
        Current media file
        Pipeline step

    Output:
        New media file
    """

    def __init__(self, workspace):

        self.workspace = workspace

    # --------------------------------------------------
    # MAIN EXECUTOR
    # --------------------------------------------------

    def execute(
        self,
        current_asset,
        pipeline_step
    ):

        operation = pipeline_step.operation

        if operation == Operation.REMOVE_AUDIO.value:
            return self.remove_audio(
                current_asset,
                pipeline_step
            )

        elif operation == Operation.REPLACE_AUDIO.value:
            return self.replace_audio(
                current_asset,
                pipeline_step
            )

        elif operation == Operation.MERGE_AUDIO.value:
            return self.merge_audio(
                current_asset,
                pipeline_step
            )

        elif operation == Operation.ADD_SUBTITLE.value:
            return self.add_subtitle(
                current_asset,
                pipeline_step
            )

        elif operation == Operation.CHANGE_THUMBNAIL.value:
            return self.change_thumbnail(
                current_asset,
                pipeline_step
            )

        raise NotImplementedError(
            f"{operation} is not implemented."
        )

    # ==================================================
    # AUDIO
    # ==================================================

    def remove_audio(
        self,
        asset,
        step
    ):

        mapper = StreamMapper(asset)

        mapper.remove_audio(
            step.data["stream_index"]
        )

        builder = FFmpegCommandBuilder()

        builder.add_input(asset.path)

        for stream in mapper.build():
            builder.add_map(stream)

        builder.copy_all()

        output = asset.path.replace(
            ".mkv",
            "_edited.mkv"
        )

        builder.set_output(output)

        command = builder.build()

        success, log = FFmpeg.run(command)

        if not success:
            raise RuntimeError(log)

        return output

    def replace_audio(
        self,
        asset,
        step
    ):
        raise NotImplementedError()

    def merge_audio(
        self,
        asset,
        step
    ):
        raise NotImplementedError()

    # ==================================================
    # SUBTITLE
    # ==================================================

    def add_subtitle(
        self,
        asset,
        step
    ):
        raise NotImplementedError()

    # ==================================================
    # THUMBNAIL
    # ==================================================

    def change_thumbnail(
        self,
        asset,
        step
    ):
        raise NotImplementedError()
