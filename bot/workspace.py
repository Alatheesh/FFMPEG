import time
from typing import Dict, Any

from core.asset_manager import AssetManager


class Workspace:

    def __init__(self):

        self.created_at = time.time()

        # All uploaded assets
        self.assets = AssetManager()

        # Main working video asset id
        self.video_asset = None

        # Pending operations
        self.pending_operations = []

        # Output settings
        self.output = {
            "filename": None,
            "container": None,
            "directory": None
        }

        # User state
        self.state = None

        # Processing state
        self.processing = False

        # Progress
        self.progress = 0


class WorkspaceManager:

    def __init__(self):

        self.workspaces: Dict[int, Workspace] = {}

    # --------------------------------

    def create(self, user_id: int):

        workspace = Workspace()

        self.workspaces[user_id] = workspace

        return workspace

    # --------------------------------

    def get(self, user_id: int):

        return self.workspaces.get(user_id)

    # --------------------------------

    def exists(self, user_id: int):

        return user_id in self.workspaces

    # --------------------------------

    def remove(self, user_id: int):

        if user_id in self.workspaces:
            del self.workspaces[user_id]

    # --------------------------------

    def clear(self):

        self.workspaces.clear()

    # --------------------------------

    def add_operation(self, user_id: int, operation):

        workspace = self.get(user_id)

        if workspace:
            workspace.pending_operations.append(operation)

    # --------------------------------

    def operation_count(self, user_id: int):

        workspace = self.get(user_id)

        if workspace:
            return len(workspace.pending_operations)

        return 0

    # --------------------------------

    def set_main_video(self, user_id: int, asset_id: str):

        workspace = self.get(user_id)

        if workspace:
            workspace.video_asset = asset_id

    # --------------------------------

    def get_main_video(self, user_id: int):

        workspace = self.get(user_id)

        if workspace:
            return workspace.assets.get(workspace.video_asset)

        return None


workspace = WorkspaceManager()
