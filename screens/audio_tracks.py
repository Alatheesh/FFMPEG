from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.media_asset import MediaAsset
from core.callback_parser import CallbackParser


class AudioTrackScreen:

    @staticmethod
    def build(
        asset: MediaAsset,
        operation: str
    ):
        """
        Build the audio track selection screen.

        operation:
            replace
            remove
            rename
            default
            extract
            swap
        """

        text = (
            "🎵 **Select Audio Track**\n\n"
            "Choose the track you want to edit.\n"
        )

        keyboard = []

        if not asset.audio_streams:

            text += "\n❌ No audio tracks found."

        else:

            for index, stream in enumerate(asset.audio_streams):

                tags = stream.get("tags", {})

                language = tags.get(
                    "language",
                    "Unknown"
                ).upper()

                title = tags.get(
                    "title",
                    ""
                )

                codec = stream.get(
                    "codec_name",
                    "Unknown"
                ).upper()

                channels = stream.get(
                    "channels",
                    "?"
                )

                disposition = stream.get(
                    "disposition",
                    {}
                )

                default = ""

                if disposition.get("default") == 1:
                    default = " ⭐"

                button_text = (
                    f"{index + 1}. "
                    f"{language} | "
                    f"{codec} | "
                    f"{channels}ch"
                    f"{default}"
                )

                if title:
                    button_text += f" ({title})"

                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=button_text,
                            callback_data=CallbackParser.build(
                                "audio",
                                operation,
                                str(index)
                            )
                        )
                    ]
                )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="menu:audio"
                ),
                InlineKeyboardButton(
                    "🏠 Home",
                    callback_data="home:open"
                )
            ]
        )

        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup(keyboard)
        }
