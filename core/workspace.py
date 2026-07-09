import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class MediaAsset(BaseModel):
    asset_id: str
    file_path: str
    file_size: int
    asset_type: str  # 'video', 'audio', 'subtitle', 'thumbnail'
    duration: Optional[float] = None
    streams: List[dict] = Field(default_factory=list)
    meta_tags: Dict[str, str] = Field(default_factory=dict)

class Operation(BaseModel):
    op_id: str
    module: str  # 'audio', 'metadata', 'subtitle'
    action: str  # 'replace_audio', 'set_title'
    parameters: dict = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

class Workspace(BaseModel):
    user_id: int
    assets: Dict[str, MediaAsset] = Field(default_factory=dict)
    pipeline: List[Operation] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)
    pending_action: Optional[str] = None  # e.g., 'waiting_for_audio_file'
    output_format: str = "mkv"
    dashboard_message_id: Optional[int] = None

class WorkspaceManager:
    def __init__(self):
        self._workspaces: Dict[int, Workspace] = {}

    def get_workspace(self, user_id: int) -> Workspace:
        if user_id not in self._workspaces:
            self._workspaces[user_id] = Workspace(user_id=user_id)
        return self._workspaces[user_id]

    def clear_workspace(self, user_id: int) -> None:
        if user_id in self._workspaces:
            del self._workspaces[user_id]
