from enum import Enum


class AssetType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"
    THUMBNAIL = "thumbnail"
    IMAGE = "image"
    ATTACHMENT = "attachment"
    UNKNOWN = "unknown"
