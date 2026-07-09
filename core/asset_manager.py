import uuid
from typing import Optional
from core.workspace import Workspace, MediaAsset

class AssetManager:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def add_asset(self, file_path: str, asset_type: str, file_size: int = 0, duration: Optional[float] = None) -> str:
        """Registers a new physical file into the workspace memory."""
        asset_id = str(uuid.uuid4())
        asset = MediaAsset(
            asset_id=asset_id,
            file_path=file_path,
            file_size=file_size,
            asset_type=asset_type,
            duration=duration
        )
        self.workspace.assets[asset_id] = asset
        self.workspace.history.append(f"Asset added: {asset_type} ({asset_id[:8]})")
        return asset_id

    def get_asset(self, asset_id: str) -> Optional[MediaAsset]:
        return self.workspace.assets.get(asset_id)

    def remove_asset(self, asset_id: str) -> bool:
        """Removes an asset from memory."""
        if asset_id in self.workspace.assets:
            del self.workspace.assets[asset_id]
            self.workspace.history.append(f"Asset removed: {asset_id[:8]}")
            return True
        return False
        
    def get_main_video(self) -> Optional[MediaAsset]:
        """Convenience method to find the primary target video."""
        for asset in self.workspace.assets.values():
            if asset.asset_type == "video":
                return asset
        return None
