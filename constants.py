from enum import Enum


# ==========================================================
# Workspace States
# ==========================================================

class WorkspaceState(str, Enum):

    IDLE = "idle"

    WAITING_VIDEO = "waiting_video"

    WAITING_AUDIO = "waiting_audio"

    WAITING_SUBTITLE = "waiting_subtitle"

    WAITING_THUMBNAIL = "waiting_thumbnail"

    WAITING_FONT = "waiting_font"

    WAITING_TRACK_SELECTION = "waiting_track_selection"

    WAITING_EXPORT = "waiting_export"

    PROCESSING = "processing"


# ==========================================================
# Asset Types
# ==========================================================

class AssetType(str, Enum):

    VIDEO = "video"

    AUDIO = "audio"

    SUBTITLE = "subtitle"

    THUMBNAIL = "thumbnail"

    FONT = "font"

    ATTACHMENT = "attachment"


# ==========================================================
# Operation Names
# ==========================================================

class Operation(str, Enum):

    # ---------- Audio ----------

    MERGE_AUDIO = "merge_audio"

    REMOVE_AUDIO = "remove_audio"

    REPLACE_AUDIO = "replace_audio"

    SWAP_AUDIO = "swap_audio"

    RENAME_AUDIO = "rename_audio"

    DEFAULT_AUDIO = "default_audio"

    EXTRACT_AUDIO = "extract_audio"

    # ---------- Subtitle ----------

    ADD_SUBTITLE = "add_subtitle"

    REMOVE_SUBTITLE = "remove_subtitle"

    REPLACE_SUBTITLE = "replace_subtitle"

    RENAME_SUBTITLE = "rename_subtitle"

    DEFAULT_SUBTITLE = "default_subtitle"

    BURN_SUBTITLE = "burn_subtitle"

    # ---------- Video ----------

    COMPRESS = "compress"

    TRIM = "trim"

    ROTATE = "rotate"

    CROP = "crop"

    RESIZE = "resize"

    CHANGE_CODEC = "change_codec"

    MERGE_VIDEO = "merge_video"

    # ---------- Thumbnail ----------

    CHANGE_THUMBNAIL = "change_thumbnail"

    REMOVE_THUMBNAIL = "remove_thumbnail"

    # ---------- Metadata ----------

    CHANGE_TITLE = "change_title"

    CHANGE_AUTHOR = "change_author"

    CHANGE_COMMENT = "change_comment"

    CHANGE_DESCRIPTION = "change_description"

    # ---------- Container ----------

    CONVERT_CONTAINER = "convert_container"

    OPTIMIZE_CONTAINER = "optimize_container"
