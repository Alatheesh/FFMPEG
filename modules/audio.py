import uuid
from core.workspace import Workspace, Operation

class AudioModule:
    @staticmethod
    def replace_audio(workspace: Workspace, audio_asset_id: str):
        """Queues an operation to completely replace the main video's audio track."""
        op = Operation(
            op_id=str(uuid.uuid4()),
            module="audio",
            action="replace_audio",
            parameters={"asset_id": audio_asset_id}
        )
        workspace.pipeline.append(op)
        workspace.history.append("Action queued: Replace Audio Track")

    @staticmethod
    def remove_audio(workspace: Workspace):
        """Queues an operation to strip all audio from the video."""
        op = Operation(
            op_id=str(uuid.uuid4()),
            module="audio",
            action="strip_audio",
            parameters={}
        )
        workspace.pipeline.append(op)
        workspace.history.append("Action queued: Strip Audio")
