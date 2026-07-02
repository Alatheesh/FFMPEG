from typing import Dict, List, Optional

from models.media_asset import MediaAsset


class AssetManager:
    """
    Central asset storage for one workspace.

    Stores every uploaded media file including:
    - Video
    - Audio
    - Subtitle
    - Thumbnail
    - Font
    - Attachment
    """

    def __init__(self):

        self.assets: Dict[str, MediaAsset] = {}

    # ==================================================
    # Add
    # ==================================================

    def add(self, asset: MediaAsset) -> str:

        self.assets[asset.id] = asset

        return asset.id

    # ==================================================
    # Remove
    # ==================================================

    def remove(self, asset_id: str):

        self.assets.pop(asset_id, None)

    # ==================================================
    # Get
    # ==================================================

    def get(self, asset_id: str) -> Optional[MediaAsset]:

        return self.assets.get(asset_id)

    # ==================================================
    # List
    # ==================================================

    def all(self) -> List[MediaAsset]:

        return list(self.assets.values())

    # ==================================================
    # First Asset
    # ==================================================

    def first(self) -> Optional[MediaAsset]:

        if not self.assets:
            return None

        return next(iter(self.assets.values()))

    # ==================================================
    # Last Asset
    # ==================================================

    def last(self) -> Optional[MediaAsset]:

        if not self.assets:
            return None

        return list(self.assets.values())[-1]

    # ==================================================
    # Filter by Type
    # ==================================================

    def by_type(self, asset_type: str) -> List[MediaAsset]:

        return [

            asset

            for asset in self.assets.values()

            if asset.type == asset_type

        ]

    # ==================================================
    # Find
    # ==================================================

    def find(self, filename: str) -> Optional[MediaAsset]:

        filename = filename.lower()

        for asset in self.assets.values():

            if asset.name.lower() == filename:

                return asset

        return None

    # ==================================================
    # Exists
    # ==================================================

    def exists(self, asset_id: str) -> bool:

        return asset_id in self.assets

    # ==================================================
    # Count
    # ==================================================

    def count(self) -> int:

        return len(self.assets)

    # ==================================================
    # Empty
    # ==================================================

    def empty(self) -> bool:

        return len(self.assets) == 0

    # ==================================================
    # Video
    # ==================================================

    def videos(self) -> List[MediaAsset]:

        return self.by_type("video")

    # ==================================================
    # Audio
    # ==================================================

    def audios(self) -> List[MediaAsset]:

        return self.by_type("audio")

    # ==================================================
    # Subtitle
    # ==================================================

    def subtitles(self) -> List[MediaAsset]:

        return self.by_type("subtitle")

    # ==================================================
    # Thumbnail
    # ==================================================

    def thumbnails(self) -> List[MediaAsset]:

        return self.by_type("thumbnail")

    # ==================================================
    # Font
    # ==================================================

    def fonts(self) -> List[MediaAsset]:

        return self.by_type("font")

    # ==================================================
    # Attachment
    # ==================================================

    def attachments(self) -> List[MediaAsset]:

        return self.by_type("attachment")

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "total": self.count(),

            "videos": len(self.videos()),

            "audios": len(self.audios()),

            "subtitles": len(self.subtitles()),

            "thumbnails": len(self.thumbnails()),

            "fonts": len(self.fonts()),

            "attachments": len(self.attachments())

        }

    # ==================================================
    # Clear
    # ==================================================

    def clear(self):

        self.assets.clear()

    # ==================================================
    # Iterator
    # ==================================================

    def __iter__(self):

        return iter(self.assets.values())

    # ==================================================
    # Length
    # ==================================================

    def __len__(self):

        return len(self.assets)

    # ==================================================
    # Contains
    # ==================================================

    def __contains__(self, asset_id: str):

        return asset_id in self.assets
