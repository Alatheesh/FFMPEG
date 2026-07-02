from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models.media_asset import MediaAsset


def audio_track_selector(
    asset: MediaAsset,
    action: str,
    allow_back: bool = True
) -> InlineKeyboardMarkup:
    """
    Create a dynamic keyboard showing all audio tracks.

    action examples:
        replace
        remove
        rename
        default
        extract
    """

    keyboard = []

    for index, stream in enumerate(asset.audio_streams):

        tags = stream.get("tags", {})

        language = tags.get("language", "Unknown").upper()

        title = tags.get("title", "")

        codec = stream.get("codec_name", "Unknown")

        default = ""

        disposition = stream.get("disposition", {})

        if disposition.get("default") == 1:
            default = " ⭐"

        text = (
            f"🎵 {index + 1}. "
            f"{language} "
            f"{codec}"
            f"{default}"
        )

        if title:
            text += f" ({title})"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"{action}:{index}"
                )
            ]
        )

    if allow_back:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="menu_audio"
                ),
                InlineKeyboardButton(
                    "🏠 Home",
                    callback_data="home"
                )
            ]
        )

    return InlineKeyboardMarkup(keyboard)
