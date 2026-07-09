import uuid
from core.workspace import Workspace, Operation

class MetadataModule:
    @staticmethod
    def set_title(workspace: Workspace, title: str):
        """Queues a title metadata update."""
        op = Operation(
            op_id=str(uuid.uuid4()),
            module="metadata",
            action="set_title",
            parameters={"title": title}
        )
        workspace.pipeline.append(op)
        workspace.history.append(f"Action queued: Set Title to '{title}'")

    @staticmethod
    def clear_all_metadata(workspace: Workspace):
        """Queues a command to wipe EXIF and existing global tags."""
        op = Operation(
            op_id=str(uuid.uuid4()),
            module="metadata",
            action="clear_metadata",
            parameters={}
        )
        workspace.pipeline.append(op)
        workspace.history.append("Action queued: Clear all metadata tags")
