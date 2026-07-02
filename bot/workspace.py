import time
from typing import Dict, Optional

from core.asset_manager import AssetManager
from core.history import HistoryManager
from core.pipeline import Pipeline
from core.pending_action import PendingActionManager


class Workspace:
    """
    Represents one user's editing workspace.
    """

    def __init__(self):

        # ----------------------------------
        # General
        # ----------------------------------

        self.created_at = time.time()

        # ----------------------------------
        # Assets
        # ----------------------------------

        self.assets = AssetManager()

        # Main video asset ID
        self.video_asset = None

        # ----------------------------------
        # History
        # ----------------------------------

        self.history = HistoryManager()

        # ----------------------------------
        # Processing Pipeline
        # ----------------------------------

        self.pipeline = Pipeline()

        # ----------------------------------
        # Pending User Action
        # ----------------------------------

        self.pending_action = PendingActionManager()

        # ----------------------------------
        # Export Settings
        # ----------------------------------

        self.output = {
            "filename": None,
            "container": None,
            "directory": None,

            "video_codec": "copy",
            "audio_codec": "copy",
            "subtitle_codec": "copy",

            "keep_metadata": True,
            "keep_thumbnail": True,
            "keep_chapters": True,
            "keep_attachments": True
        }

        # ----------------------------------
        # Runtime
        # ----------------------------------

        self.processing = False

        self.progress = 0

    # ==================================================
    # Main Video
    # ==================================================

    def set_main_video(self, asset):

        if hasattr(asset, "id"):
            self.video_asset = asset.id
        else:
            self.video_asset = asset

    def get_main_video(self):

        if self.video_asset is None:
            return None

        return self.assets.get(self.video_asset)

    # ==================================================
    # Assets
    # ==================================================

    def add_asset(self, asset):

        return self.assets.add(asset)

    def remove_asset(self, asset_id: str):

        self.assets.remove(asset_id)

    def get_asset(self, asset_id: str):

        return self.assets.get(asset_id)

    def get_assets(self):

        return self.assets.all()

    def get_assets_by_type(self, asset_type: str):

        return self.assets.by_type(asset_type)

    def asset_exists(self, asset_id: str):

        return self.assets.exists(asset_id)

    def asset_count(self):

        return self.assets.count()

    # ==================================================
    # Processing
    # ==================================================

    def start_processing(self):

        self.processing = True
        self.progress = 0

    def finish_processing(self):

        self.processing = False
        self.progress = 100

    def reset_progress(self):

        self.progress = 0

    def reset(self):

        self.clear()

    # ==================================================
    # Workspace
    # ==================================================

    def clear(self):

        self.assets.clear()

        self.history.clear()

        self.pipeline.clear()

        self.pending_action.clear()

        self.video_asset = None

        self.processing = False

        self.progress = 0


class WorkspaceManager:

    def __init__(self):

        self.workspaces: Dict[int, Workspace] = {}

    # ==================================================
    # Create
    # ==================================================

    def create(self, user_id: int) -> Workspace:

        workspace = Workspace()

        self.workspaces[user_id] = workspace

        return workspace

    # ==================================================
    # Get
    # ==================================================

    def get(self, user_id: int) -> Optional[Workspace]:

        return self.workspaces.get(user_id)

    # ==================================================
    # Get or Create
    # ==================================================

    def get_or_create(self, user_id: int) -> Workspace:

        workspace = self.get(user_id)

        if workspace is None:
            workspace = self.create(user_id)

        return workspace

    # ==================================================
    # Exists
    # ==================================================

    def exists(self, user_id: int) -> bool:

        return user_id in self.workspaces

    # ==================================================
    # Remove
    # ==================================================

    def remove(self, user_id: int):

        self.workspaces.pop(user_id, None)

    # ==================================================
    # Clear All
    # ==================================================

    def clear(self):

        self.workspaces.clear()

    # ==================================================
    # Count
    # ==================================================

    def count(self):

        return len(self.workspaces)


workspace = WorkspaceManager()
