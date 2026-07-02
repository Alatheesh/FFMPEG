from typing import List, Optional
from constants import Operation
from core.operation_queue import OperationQueue
from core.validator import Validator


class AudioManager:
    """
    Handles every audio related operation.

    Supported Operations
    --------------------
    • Remove Audio
    • Replace Audio
    • Merge Audio
    • Swap Audio
    • Rename Audio
    • Set Default Audio
    • Extract Audio
    """

    def __init__(self, workspace):
        self.workspace = workspace
        self.queue = OperationQueue(workspace)
        self.validator = Validator(workspace)

    # =====================================================
    # Helpers
    # =====================================================

    def _main_video(self):
        video = self.workspace.get_main_video()
        if not video:
            raise ValueError("No video found in workspace.")
        return video

    def _validate_stream(self, stream_index: int):
        video = self._main_video()

        if stream_index < 0:
            raise ValueError("Invalid stream index.")

        streams = [
            s["index"]
            for s in video.audio_streams
        ]

        if stream_index not in streams:
            raise ValueError(
                f"Audio stream {stream_index} not found."
            )

        return video

    def _validate_asset(self, asset_id: str):
        asset = self.workspace.assets.get(asset_id)

        if asset is None:
            raise ValueError(
                f"Asset {asset_id} does not exist."
            )

        return asset

    def _queue(
        self,
        operation: Operation,
        data: dict
    ):
        return self.queue.add(
            operation,
            data
        )

    # =====================================================
    # Remove Audio
    # =====================================================

    def remove(
        self,
        stream_index: int
    ):

        self._validate_stream(stream_index)

        return self._queue(
            Operation.REMOVE_AUDIO,
            {
                "stream_index": stream_index
            }
        )

    # =====================================================
    # Replace Audio
    # =====================================================

    def replace(
        self,
        stream_index: int,
        audio_asset_id: str
    ):

        self._validate_stream(stream_index)

        self._validate_asset(audio_asset_id)

        return self._queue(
            Operation.REPLACE_AUDIO,
            {
                "stream_index": stream_index,
                "audio_asset_id": audio_asset_id
            }
        )

    # =====================================================
    # Merge Audio
    # =====================================================

    def merge(
        self,
        audio_asset_ids: List[str]
    ):

        if not audio_asset_ids:
            raise ValueError(
                "No audio assets supplied."
            )

        for asset_id in audio_asset_ids:
            self._validate_asset(asset_id)

        return self._queue(
            Operation.MERGE_AUDIO,
            {
                "audio_asset_ids": audio_asset_ids
            }
        )

    # =====================================================
    # Swap Audio
    # =====================================================

    def swap(
        self,
        first_stream: int,
        second_stream: int
    ):

        self._validate_stream(first_stream)
        self._validate_stream(second_stream)

        if first_stream == second_stream:
            raise ValueError(
                "Cannot swap the same stream."
            )

        return self._queue(
            Operation.SWAP_AUDIO,
            {
                "first_stream": first_stream,
                "second_stream": second_stream
            }
        )

    # =====================================================
    # Rename Audio
    # =====================================================

    def rename(
        self,
        stream_index: int,
        title: str
    ):

        self._validate_stream(stream_index)

        title = title.strip()

        if not title:
            raise ValueError(
                "Track title cannot be empty."
            )

        return self._queue(
            Operation.RENAME_AUDIO,
            {
                "stream_index": stream_index,
                "title": title
            }
        )

    # =====================================================
    # Set Default Audio
    # =====================================================

    def set_default(
        self,
        stream_index: int
    ):

        self._validate_stream(stream_index)

        return self._queue(
            Operation.DEFAULT_AUDIO,
            {
                "stream_index": stream_index
            }
        )

    # =====================================================
    # Extract Audio
    # =====================================================

    def extract(
        self,
        stream_index: int
    ):

        self._validate_stream(stream_index)

        return self._queue(
            Operation.EXTRACT_AUDIO,
            {
                "stream_index": stream_index
            }
        )

    # =====================================================
    # Queue Helpers
    # =====================================================

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
        operation_id: str
    ):

        self.queue.remove(operation_id)

    # =====================================================
    # Search Helpers
    # =====================================================

    def find_by_operation(
        self,
        operation: Operation
    ):

        return [
            item
            for item in self.pending()
            if item.operation == operation.value
        ]

    def has_operation(
        self,
        operation: Operation
    ):

        return len(
            self.find_by_operation(operation)
        ) > 0

    # =====================================================
    # Duplicate Validation
    # =====================================================

    def has_pending_remove(
        self,
        stream_index: int
    ):

        for item in self.pending():

            if (
                item.operation ==
                Operation.REMOVE_AUDIO.value
            ):

                if (
                    item.data.get("stream_index")
                    == stream_index
                ):
                    return True

        return False

    def has_pending_replace(
        self,
        stream_index: int
    ):

        for item in self.pending():

            if (
                item.operation ==
                Operation.REPLACE_AUDIO.value
            ):

                if (
                    item.data.get("stream_index")
                    == stream_index
                ):
                    return True

        return False

      # =====================================================
    # Batch Operations
    # =====================================================

    def remove_many(
        self,
        stream_indexes: List[int]
    ):

        results=[]

        for stream_index in stream_indexes:
            results.append(
                self.remove(stream_index)
            )

        return results

    def extract_many(
        self,
        stream_indexes: List[int]
    ):

        results=[]

        for stream_index in stream_indexes:
            results.append(
                self.extract(stream_index)
            )

        return results

    # =====================================================
    # Language
    # =====================================================

    def set_language(
        self,
        stream_index:int,
        language:str
    ):

        self._validate_stream(stream_index)

        language=language.strip().lower()

        if not language:
            raise ValueError("Language cannot be empty.")

        return self._queue(
            Operation.RENAME_AUDIO,
            {
                "stream_index":stream_index,
                "language":language,
                "metadata_only":True
            }
        )

    # =====================================================
    # Track Flags
    # =====================================================

    def set_forced(
        self,
        stream_index:int,
        enabled:bool=True
    ):

        self._validate_stream(stream_index)

        return self._queue(
            Operation.DEFAULT_AUDIO,
            {
                "stream_index":stream_index,
                "forced":enabled
            }
        )

    def unset_default(
        self,
        stream_index:int
    ):

        self._validate_stream(stream_index)

        return self._queue(
            Operation.DEFAULT_AUDIO,
            {
                "stream_index":stream_index,
                "default":False
            }
        )

    # =====================================================
    # Validation Helpers
    # =====================================================

    def stream_exists(
        self,
        stream_index:int
    )->bool:

        try:
            self._validate_stream(stream_index)
            return True
        except Exception:
            return False

    def asset_exists(
        self,
        asset_id:str
    )->bool:

        return self.workspace.assets.get(asset_id) is not None

    # =====================================================
    # Information
    # =====================================================

    def audio_tracks(self):

        video=self._main_video()

        return video.audio_streams

    def track_count(self):

        return len(
            self.audio_tracks()
        )

    def get_track(
        self,
        stream_index:int
    ):

        for stream in self.audio_tracks():

            if stream["index"]==stream_index:
                return stream

        return None

    # =====================================================
    # Queue Summary
    # =====================================================

    def summary(self):

        summary=[]

        for item in self.pending():

            summary.append({
                "id":item.id,
                "operation":item.operation,
                "data":item.data,
                "status":item.status
            })

        return summary

    # =====================================================
    # Queue Statistics
    # =====================================================

    def statistics(self):

        stats={
            "remove":0,
            "replace":0,
            "merge":0,
            "swap":0,
            "rename":0,
            "default":0,
            "extract":0
        }

        for item in self.pending():

            op=item.operation

            if op==Operation.REMOVE_AUDIO.value:
                stats["remove"]+=1

            elif op==Operation.REPLACE_AUDIO.value:
                stats["replace"]+=1

            elif op==Operation.MERGE_AUDIO.value:
                stats["merge"]+=1

            elif op==Operation.SWAP_AUDIO.value:
                stats["swap"]+=1

            elif op==Operation.RENAME_AUDIO.value:
                stats["rename"]+=1

            elif op==Operation.DEFAULT_AUDIO.value:
                stats["default"]+=1

            elif op==Operation.EXTRACT_AUDIO.value:
                stats["extract"]+=1

        stats["total"]=sum(stats.values())

        return stats

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.clear()

    # =====================================================
    # String Representation
    # =====================================================

    def __len__(self):

        return self.pending_count()

    def __bool__(self):

        return self.pending_count()>0

      # =====================================================
    # Conflict Detection
    # =====================================================

    def conflicts(self):

        conflicts=[]

        pending=self.pending()

        for i,item1 in enumerate(pending):

            for item2 in pending[i+1:]:

                if item1.data.get("stream_index")!=item2.data.get("stream_index"):
                    continue

                if item1.operation==item2.operation:

                    conflicts.append({
                        "type":"duplicate",
                        "first":item1.id,
                        "second":item2.id,
                        "operation":item1.operation
                    })

                elif (
                    item1.operation==Operation.REMOVE_AUDIO.value and
                    item2.operation in (
                        Operation.REPLACE_AUDIO.value,
                        Operation.RENAME_AUDIO.value,
                        Operation.DEFAULT_AUDIO.value
                    )
                ):

                    conflicts.append({
                        "type":"remove_conflict",
                        "first":item1.id,
                        "second":item2.id
                    })

        return conflicts

    # =====================================================
    # Export Helpers
    # =====================================================

    def export_operations(self):

        operations=[]

        for item in self.pending():

            operations.append({
                "id":item.id,
                "operation":item.operation,
                "data":item.data
            })

        return operations

    def has_conflicts(self):

        return len(self.conflicts())>0

    def ready_for_export(self):

        return (
            self.pending_count()>0 and
            not self.has_conflicts()
        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(self,engine):

        if not self.ready_for_export():
            raise RuntimeError(
                "Audio queue contains conflicts or is empty."
            )

        return engine.process_audio(
            self.export_operations()
        )

    # =====================================================
    # Debug
    # =====================================================

    def print_queue(self):

        for index,item in enumerate(self.pending(),1):

            print(
                f"[{index}] "
                f"{item.operation} "
                f"{item.data}"
            )

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {
            "pending":self.export_operations(),
            "statistics":self.statistics(),
            "conflicts":self.conflicts()
        }

    @classmethod
    def from_workspace(cls,workspace):

        return cls(workspace)

    # =====================================================
    # Magic Methods
    # =====================================================

    def __iter__(self):

        return iter(self.pending())

    def __contains__(self,operation):

        if isinstance(operation,Operation):
            operation=operation.value

        return any(
            item.operation==operation
            for item in self.pending()
        )

    def __repr__(self):

        return (
            f"<AudioManager "
            f"pending={self.pending_count()} "
            f"tracks={self.track_count()}>"
        )
