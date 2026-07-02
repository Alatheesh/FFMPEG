from typing import List, Optional
from constants import Operation
from core.operation_queue import OperationQueue
from core.validator import Validator


class MediaManager:

    """
    Handles every non-audio media operation.

    Supported

    Subtitle
        Add
        Remove
        Replace
        Rename
        Burn
        Default

    Video
        Trim
        Crop
        Resize
        Rotate
        Compress
        Merge

    Thumbnail
        Replace
        Remove
        Extract

    Metadata
        Title
        Author
        Description
        Comment
        Copyright

    Container
        MP4
        MKV
        AVI
        MOV
    """

    def __init__(self,workspace):

        self.workspace=workspace
        self.queue=OperationQueue(workspace)
        self.validator=Validator(workspace)

    # ====================================================
    # Helpers
    # ====================================================

    def _video(self):

        video=self.workspace.get_main_video()

        if video is None:
            raise ValueError(
                "No video loaded."
            )

        return video

    def _asset(self,asset_id):

        asset=self.workspace.assets.get(asset_id)

        if asset is None:
            raise ValueError(
                f"Asset {asset_id} not found."
            )

        return asset

    def _queue(self,operation,data):

        return self.queue.add(
            operation,
            data
        )

    # ====================================================
    # Subtitle
    # ====================================================

    def add_subtitle(
        self,
        subtitle_asset_id:str,
        language:str="und",
        default:bool=False
    ):

        self._video()
        self._asset(subtitle_asset_id)

        return self._queue(
            Operation.ADD_SUBTITLE,
            {
                "subtitle_asset_id":subtitle_asset_id,
                "language":language,
                "default":default
            }
        )

    def remove_subtitle(
        self,
        stream_index:int
    ):

        self._video()

        return self._queue(
            Operation.REMOVE_SUBTITLE,
            {
                "stream_index":stream_index
            }
        )

    def replace_subtitle(
        self,
        stream_index:int,
        subtitle_asset_id:str
    ):

        self._video()
        self._asset(subtitle_asset_id)

        return self._queue(
            Operation.REPLACE_SUBTITLE,
            {
                "stream_index":stream_index,
                "subtitle_asset_id":subtitle_asset_id
            }
        )

    def rename_subtitle(
        self,
        stream_index:int,
        title:str
    ):

        self._video()

        if not title.strip():
            raise ValueError(
                "Subtitle title cannot be empty."
            )

        return self._queue(
            Operation.RENAME_SUBTITLE,
            {
                "stream_index":stream_index,
                "title":title.strip()
            }
        )

    def burn_subtitle(
        self,
        subtitle_asset_id:str
    ):

        self._video()
        self._asset(subtitle_asset_id)

        return self._queue(
            Operation.BURN_SUBTITLE,
            {
                "subtitle_asset_id":subtitle_asset_id
            }
        )

    # ====================================================
    # Video
    # ====================================================

    def trim(
        self,
        start:str,
        end:str
    ):

        self._video()

        return self._queue(
            Operation.TRIM_VIDEO,
            {
                "start":start,
                "end":end
            }
        )

    def crop(
        self,
        width:int,
        height:int,
        x:int,
        y:int
    ):

        self._video()

        return self._queue(
            Operation.CROP_VIDEO,
            {
                "width":width,
                "height":height,
                "x":x,
                "y":y
            }
        )

    def resize(
        self,
        width:int,
        height:int
    ):

        self._video()

        return self._queue(
            Operation.RESIZE_VIDEO,
            {
                "width":width,
                "height":height
            }
        )
    # ====================================================
    # Video
    # ====================================================

    def rotate(
        self,
        angle:int
    ):

        self._video()

        if angle not in (90,180,270):
            raise ValueError(
                "Rotation must be 90, 180 or 270."
            )

        return self._queue(
            Operation.ROTATE_VIDEO,
            {
                "angle":angle
            }
        )

    def compress(
        self,
        video_codec:str="libx264",
        audio_codec:str="aac",
        crf:int=23,
        preset:str="medium"
    ):

        self._video()

        return self._queue(
            Operation.COMPRESS_VIDEO,
            {
                "video_codec":video_codec,
                "audio_codec":audio_codec,
                "crf":crf,
                "preset":preset
            }
        )

    def merge_video(
        self,
        video_asset_ids:List[str]
    ):

        if len(video_asset_ids)<2:
            raise ValueError(
                "At least two videos are required."
            )

        for asset_id in video_asset_ids:
            self._asset(asset_id)

        return self._queue(
            Operation.MERGE_VIDEO,
            {
                "video_asset_ids":video_asset_ids
            }
        )

    def change_speed(
        self,
        speed:float
    ):

        self._video()

        if speed<=0:
            raise ValueError(
                "Speed must be greater than zero."
            )

        return self._queue(
            Operation.CHANGE_SPEED,
            {
                "speed":speed
            }
        )

    # ====================================================
    # Thumbnail
    # ====================================================

    def replace_thumbnail(
        self,
        image_asset_id:str
    ):

        self._video()
        self._asset(image_asset_id)

        return self._queue(
            Operation.CHANGE_THUMBNAIL,
            {
                "image_asset_id":image_asset_id
            }
        )

    def remove_thumbnail(self):

        self._video()

        return self._queue(
            Operation.REMOVE_THUMBNAIL,
            {}
        )

    def extract_thumbnail(
        self,
        timestamp:str="00:00:05"
    ):

        self._video()

        return self._queue(
            Operation.EXTRACT_THUMBNAIL,
            {
                "timestamp":timestamp
            }
        )

    # ====================================================
    # Metadata
    # ====================================================

    def set_title(
        self,
        title:str
    ):

        self._video()

        return self._queue(
            Operation.SET_TITLE,
            {
                "title":title.strip()
            }
        )

    def set_author(
        self,
        author:str
    ):

        self._video()

        return self._queue(
            Operation.SET_AUTHOR,
            {
                "author":author.strip()
            }
        )

    def set_description(
        self,
        description:str
    ):

        self._video()

        return self._queue(
            Operation.SET_DESCRIPTION,
            {
                "description":description.strip()
            }
        )

    def set_comment(
        self,
        comment:str
    ):

        self._video()

        return self._queue(
            Operation.SET_COMMENT,
            {
                "comment":comment.strip()
            }
        )

    def set_copyright(
        self,
        copyright:str
    ):

        self._video()

        return self._queue(
            Operation.SET_COPYRIGHT,
            {
                "copyright":copyright.strip()
            }
        )

    def set_encoder(
        self,
        encoder:str
    ):

        self._video()

        return self._queue(
            Operation.SET_ENCODER,
            {
                "encoder":encoder.strip()
            }
        )
    # ====================================================
    # Container
    # ====================================================

    def convert_container(
        self,
        container:str
    ):

        self._video()

        container=container.lower().replace(".","")

        if container not in (
            "mkv",
            "mp4",
            "mov",
            "avi",
            "webm"
        ):
            raise ValueError(
                "Unsupported container."
            )

        return self._queue(
            Operation.CONVERT_CONTAINER,
            {
                "container":container
            }
        )

    # ====================================================
    # Queue Helpers
    # ====================================================

    def pending(self):

        return self.queue.pending()

    def completed(self):

        return self.queue.completed()

    def pending_count(self):

        return self.queue.pending_count()

    def clear(self):

        self.queue.clear()

    def remove_operation(
        self,
        operation_id:str
    ):

        self.queue.remove(operation_id)

    # ====================================================
    # Search Helpers
    # ====================================================

    def find_by_operation(
        self,
        operation
    ):

        if hasattr(operation,"value"):
            operation=operation.value

        return [
            item
            for item in self.pending()
            if item.operation==operation
        ]

    def has_operation(
        self,
        operation
    ):

        return len(
            self.find_by_operation(operation)
        )>0

    # ====================================================
    # Validation
    # ====================================================

    def validate_workspace(self):

        self._video()

        return True

    def validate_asset(
        self,
        asset_id:str
    ):

        return self._asset(asset_id)

    # ====================================================
    # Summary
    # ====================================================

    def summary(self):

        result=[]

        for item in self.pending():

            result.append({
                "id":item.id,
                "operation":item.operation,
                "data":item.data,
                "status":item.status
            })

        return result

    # ====================================================
    # Statistics
    # ====================================================

    def statistics(self):

        stats={}

        for item in self.pending():

            stats[item.operation]=(
                stats.get(item.operation,0)+1
            )

        stats["total"]=self.pending_count()

        return stats

    # ====================================================
    # Conflict Detection
    # ====================================================

    def conflicts(self):

        conflicts=[]

        pending=self.pending()

        for i,item1 in enumerate(pending):

            for item2 in pending[i+1:]:

                if (
                    item1.operation==
                    item2.operation
                ):

                    if item1.data==item2.data:

                        conflicts.append({
                            "type":"duplicate",
                            "first":item1.id,
                            "second":item2.id,
                            "operation":item1.operation
                        })

        return conflicts

    def has_conflicts(self):

        return len(
            self.conflicts()
        )>0

    def ready_for_export(self):

        return (
            self.pending_count()>0 and
            not self.has_conflicts()
        )

    # ====================================================
    # Batch Helpers
    # ====================================================

    def remove_many_subtitles(
        self,
        stream_indexes:List[int]
    ):

        result=[]

        for stream in stream_indexes:
            result.append(
                self.remove_subtitle(stream)
            )

        return result

    def batch_convert(
        self,
        asset_ids:List[str],
        container:str
    ):

        jobs=[]

        for asset_id in asset_ids:

            self._asset(asset_id)

            jobs.append(
                self._queue(
                    Operation.CONVERT_CONTAINER,
                    {
                        "asset_id":asset_id,
                        "container":container
                    }
                )
            )

        return jobs
    # ====================================================
    # Export Helpers
    # ====================================================

    def export_operations(self):

        operations=[]

        for item in self.pending():

            operations.append({
                "id":item.id,
                "operation":item.operation,
                "data":item.data
            })

        return operations

    def export_summary(self):

        return {
            "operations":self.export_operations(),
            "statistics":self.statistics(),
            "conflicts":self.conflicts(),
            "ready":self.ready_for_export()
        }

    # ====================================================
    # Execution Bridge
    # ====================================================

    def execute(
        self,
        media_engine
    ):

        if not self.ready_for_export():
            raise RuntimeError(
                "Pending operations contain conflicts."
            )

        return media_engine.process_media(
            self.export_operations()
        )

    # ====================================================
    # Queue Editing
    # ====================================================

    def move_up(
        self,
        operation_id:str
    ):

        operations=self.pending()

        for index,item in enumerate(operations):

            if item.id!=operation_id:
                continue

            if index==0:
                return False

            operations[index],operations[index-1]=(
                operations[index-1],
                operations[index]
            )

            return True

        return False

    def move_down(
        self,
        operation_id:str
    ):

        operations=self.pending()

        for index,item in enumerate(operations):

            if item.id!=operation_id:
                continue

            if index>=len(operations)-1:
                return False

            operations[index],operations[index+1]=(
                operations[index+1],
                operations[index]
            )

            return True

        return False

    # ====================================================
    # Reset
    # ====================================================

    def reset(self):

        self.clear()

    # ====================================================
    # Debug
    # ====================================================

    def print_queue(self):

        for index,item in enumerate(self.pending(),1):

            print(
                f"[{index}] "
                f"{item.operation} "
                f"{item.data}"
            )

    # ====================================================
    # Serialization
    # ====================================================

    def to_dict(self):

        return {
            "operations":self.export_operations(),
            "statistics":self.statistics(),
            "conflicts":self.conflicts()
        }

    @classmethod
    def from_workspace(
        cls,
        workspace
    ):

        return cls(workspace)

    # ====================================================
    # Magic Methods
    # ====================================================

    def __len__(self):

        return self.pending_count()

    def __iter__(self):

        return iter(self.pending())

    def __bool__(self):

        return self.pending_count()>0

    def __contains__(
        self,
        operation
    ):

        if hasattr(operation,"value"):
            operation=operation.value

        return any(
            item.operation==operation
            for item in self.pending()
        )

    def __repr__(self):

        return (
            f"<MediaManager "
            f"pending={self.pending_count()} "
            f"conflicts={len(self.conflicts())}>"
        )
