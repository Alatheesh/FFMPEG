from constants import Operation
from core.operation_queue import OperationQueue


class AudioOperationManager:

    def __init__(self, workspace):

        self.workspace = workspace

        self.queue = OperationQueue(workspace)

    # ------------------------------------------------
    # Remove Audio
    # ------------------------------------------------

    def remove(
        self,
        stream_index: int
    ):

        return self.queue.add(
            Operation.REMOVE_AUDIO,
            {
                "stream_index": stream_index
            }
        )

    # ------------------------------------------------
    # Replace Audio
    # ------------------------------------------------

    def replace(
        self,
        stream_index: int,
        audio_asset_id: str
    ):

        return self.queue.add(
            Operation.REPLACE_AUDIO,
            {
                "stream_index": stream_index,
                "audio_asset_id": audio_asset_id
            }
        )

    # ------------------------------------------------
    # Merge Audio
    # ------------------------------------------------

    def merge(
        self,
        audio_asset_ids: list
    ):

        return self.queue.add(
            Operation.MERGE_AUDIO,
            {
                "audio_asset_ids": audio_asset_ids
            }
        )

    # ------------------------------------------------
    # Rename Track
    # ------------------------------------------------

    def rename(
        self,
        stream_index: int,
        new_name: str
    ):

        return self.queue.add(
            Operation.RENAME_AUDIO,
            {
                "stream_index": stream_index,
                "new_name": new_name
            }
        )

    # ------------------------------------------------
    # Default Track
    # ------------------------------------------------

    def default(
        self,
        stream_index: int
    ):

        return self.queue.add(
            Operation.DEFAULT_AUDIO,
            {
                "stream_index": stream_index
            }
        )

    # ------------------------------------------------
    # Swap
    # ------------------------------------------------

    def swap(
        self,
        first_stream: int,
        second_stream: int
    ):

        return self.queue.add(
            Operation.SWAP_AUDIO,
            {
                "first_stream": first_stream,
                "second_stream": second_stream
            }
        )

    # ------------------------------------------------
    # Extract
    # ------------------------------------------------

    def extract(
        self,
        stream_index: int
    ):

        return self.queue.add(
            Operation.EXTRACT_AUDIO,
            {
                "stream_index": stream_index
            }
        )
