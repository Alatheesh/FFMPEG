from constants import Operation


def queue_remove_audio(
    workspace,
    track_index: int
):
    """
    Queue an audio track for removal.
    """

    video = workspace.get_main_video()

    if not video:
        raise ValueError("No main video selected.")

    operation = {
        "operation": Operation.REMOVE_AUDIO.value,

        "track_index": track_index,

        "video_asset_id": video.id
    }

    history_item = workspace.history.add(
        operation=Operation.REMOVE_AUDIO.value,
        data=operation
    )

    return history_item
