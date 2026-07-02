from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


@dataclass
class MediaAsset:
    """
    Represents one uploaded media file.
    """

    # Unique asset id
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Basic information
    name: str = ""
    path: str = ""
    type: str = ""

    # File information
    size: int = 0
    duration: float = 0

    # Media information
    format: str = ""
    container: str = ""

    # Parsed streams
    video_streams: List[Dict] = field(default_factory=list)
    audio_streams: List[Dict] = field(default_factory=list)
    subtitle_streams: List[Dict] = field(default_factory=list)
    attachment_streams: List[Dict] = field(default_factory=list)

    # Extra metadata
    metadata: Dict = field(default_factory=dict)

    # Temporary files generated from this asset
    temp_files: List[str] = field(default_factory=list)

    def add_temp_file(self, path: str):
        self.temp_files.append(path)

    def remove_temp_file(self, path: str):
        if path in self.temp_files:
            self.temp_files.remove(path)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "type": self.type,
            "size": self.size,
            "duration": self.duration,
            "format": self.format,
            "container": self.container,
            "video_streams": self.video_streams,
            "audio_streams": self.audio_streams,
            "subtitle_streams": self.subtitle_streams,
            "attachment_streams": self.attachment_streams,
            "metadata": self.metadata,
        }
