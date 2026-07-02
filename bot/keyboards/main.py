from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎵 Audio",
                    callback_data="menu_audio"
                ),
                InlineKeyboardButton(
                    "💬 Subtitles",
                    callback_data="menu_subtitle"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎥 Video",
                    callback_data="menu_video"
                ),
                InlineKeyboardButton(
                    "📦 Container",
                    callback_data="menu_container"
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 Metadata",
                    callback_data="menu_metadata"
                ),
                InlineKeyboardButton(
                    "🖼 Thumbnail",
                    callback_data="menu_thumbnail"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ Media Information",
                    callback_data="media_info"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel_job"
                )
            ]
        ]
    )

    return keyboard
