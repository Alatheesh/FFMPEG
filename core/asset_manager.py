from typing import Dict, List, Optional

from models.media_asset import MediaAsset


class AssetManager:

    def __init__(self):
        self.assets: Dict[str, MediaAsset] = {}

    # ----------------------------------
    # Add
    # ----------------------------------

    def add(self, asset: MediaAsset):

        self.assets[asset.id] = asset

        return asset.id

    # ----------------------------------
    # Remove
    # ----------------------------------

    def remove(self, asset_id: str):

        if asset_id in self.assets:
            del self.assets[asset_id]

    # ----------------------------------
    # Get
    # ----------------------------------

    def get(self, asset_id: str) -> Optional[MediaAsset]:

        return self.assets.get(asset_id)

    # ----------------------------------
    # List
    # ----------------------------------

    def all(self) -> List[MediaAsset]:

        return list(self.assets.values())

    # ----------------------------------
    # Filter by type
    # ----------------------------------

    def by_type(self, asset_type: str) -> List[MediaAsset]:

        return [
            asset
            for asset in self.assets.values()
            if asset.type == asset_type
        ]

    # ----------------------------------
    # Count
    # ----------------------------------

    def count(self):

        return len(self.assets)

    # ----------------------------------
    # Exists
    # ----------------------------------

    def exists(self, asset_id: str):

        return asset_id in self.assets

    # ----------------------------------
    # Clear
    # ----------------------------------

    def clear(self):

        self.assets.clear()

    # ----------------------------------
    # Find by filename
    # ----------------------------------

    def find(self, filename: str):

        for asset in self.assets.values():

            if asset.name == filename:
                return asset

        return None

    # ----------------------------------
    # Summary
    # ----------------------------------

    def summary(self):

        return {
            "videos": len(self.by_type("video")),
            "audios": len(self.by_type("audio")),
            "subtitles": len(self.by_type("subtitle")),
            "thumbnails": len(self.by_type("thumbnail")),
            "fonts": len(self.by_type("font")),
            "attachments": len(self.by_type("attachment"))
        }
