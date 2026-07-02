from models.media_asset import MediaAsset


def bytes_to_size(size: int) -> str:
    """
    Convert bytes into a readable size.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def milliseconds_to_time(ms):

    if not ms:
        return "Unknown"

    seconds = int(ms / 1000)

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h > 0:
        return f"{h}h {m}m {s}s"

    return f"{m}m {s}s"


def create_summary(asset: MediaAsset):

    text = []

    text.append("🎬 **Media Information**\n")

    text.append(f"📄 **Name:** `{asset.name}`")

    text.append(f"📦 **Size:** `{bytes_to_size(asset.size)}`")

    text.append(
        f"⏱ **Duration:** `{milliseconds_to_time(asset.duration)}`"
    )

    text.append(
        f"🎥 **Video Tracks:** `{len(asset.video_streams)}`"
    )

    text.append(
        f"🎵 **Audio Tracks:** `{len(asset.audio_streams)}`"
    )

    text.append(
        f"💬 **Subtitle Tracks:** `{len(asset.subtitle_streams)}`"
    )

    # ---------------- Video ----------------

    if asset.video_streams:

        text.append("\n🎥 **Video**")

        for i, stream in enumerate(asset.video_streams, start=1):

            width = stream.get("width", "?")
            height = stream.get("height", "?")
            codec = stream.get("codec_name", "Unknown")

            text.append(
                f"{i}. {codec} • {width}×{height}"
            )

    # ---------------- Audio ----------------

    if asset.audio_streams:

        text.append("\n🎵 **Audio**")

        for i, stream in enumerate(asset.audio_streams, start=1):

            lang = (
                stream.get("tags", {})
                .get("language", "Unknown")
            )

            codec = stream.get(
                "codec_name",
                "Unknown"
            )

            text.append(
                f"{i}. {lang} • {codec}"
            )

    # --------------- Subtitle ---------------

    if asset.subtitle_streams:

        text.append("\n💬 **Subtitles**")

        for i, stream in enumerate(asset.subtitle_streams, start=1):

            lang = (
                stream.get("tags", {})
                .get("language", "Unknown")
            )

            codec = stream.get(
                "codec_name",
                "Unknown"
            )

            text.append(
                f"{i}. {lang} • {codec}"
            )

    return "\n".join(text)
