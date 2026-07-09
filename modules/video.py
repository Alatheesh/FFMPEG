import uuid
from core.workspace import Workspace, Operation

class VideoModule:
    @staticmethod
    def apply_compression(workspace: Workspace, crf: int = 23, preset: str = "medium"):
        """Queues a re-encoding operation with specific compression targets."""
        op = Operation(
            op_id=str(uuid.uuid4()),
            module="video",
            action="compress",
            parameters={"crf": crf, "preset": preset}
        )
        workspace.pipeline.append(op)
        workspace.history.append(f"Action queued: Compress (CRF {crf}, Preset: {preset})")
