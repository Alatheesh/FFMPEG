from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


@dataclass
class MediaAsset:
    """
    Represents one uploaded media asset.
    """

    # ==================================================
    # Identity
    # ==================================================

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # ==================================================
    # Basic Information
    # ==================================================

    name: str = ""
    original_name: str = ""
    path: str = ""
    type: str = ""

    # ==================================================
    # File Information
    # ==================================================

    size: int = 0
    duration: float = 0

    format: str = ""
    container: str = ""
    mime_type: str = ""

    # ==================================================
    # Telegram Information
    # ==================================================

    telegram_file_id: str = ""
    telegram_unique_id: str = ""

    # ==================================================
    # Parsed Streams
    # ==================================================

    video_streams: List[Dict] = field(default_factory=list)
    audio_streams: List[Dict] = field(default_factory=list)
    subtitle_streams: List[Dict] = field(default_factory=list)
    attachment_streams: List[Dict] = field(default_factory=list)

    # ==================================================
    # FFprobe Metadata
    # ==================================================

    metadata: Dict = field(default_factory=dict)

    # ==================================================
    # Thumbnail
    # ==================================================

    thumbnail: Optional[str] = None

    # ==================================================
    # Temporary Files
    # ==================================================

    temp_files: List[str] = field(default_factory=list)

    # ==================================================
    # State
    # ==================================================

    modified: bool = False

    # ==================================================
    # Helpers
    # ==================================================

    def mark_modified(self):

        self.modified = True

    def set_thumbnail(self, path: str):

        self.thumbnail = path

        self.modified = True

    def add_temp_file(self, path: str):

        if path not in self.temp_files:
            self.temp_files.append(path)

    def remove_temp_file(self, path: str):

        if path in self.temp_files:
            self.temp_files.remove(path)

    # ==================================================
    # Properties
    # ==================================================

    @property
    def video_count(self):

        return len(self.video_streams)

    @property
    def audio_count(self):

        return len(self.audio_streams)

    @property
    def subtitle_count(self):

        return len(self.subtitle_streams)

    @property
    def attachment_count(self):

        return len(self.attachment_streams)

    # ==================================================
    # Serialization
    # ==================================================

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "original_name": self.original_name,

            "path": self.path,

            "type": self.type,

            "size": self.size,

            "duration": self.duration,

            "format": self.format,

            "container": self.container,

            "mime_type": self.mime_type,

            "telegram_file_id": self.telegram_file_id,

            "telegram_unique_id": self.telegram_unique_id,

            "video_streams": self.video_streams,

            "audio_streams": self.audio_streams,

            "subtitle_streams": self.subtitle_streams,

            "attachment_streams": self.attachment_streams,

            "metadata": self.metadata,

            "thumbnail": self.thumbnail,

            "modified": self.modified,

            "temp_files": self.temp_files
        }
