from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def audio_menu(audio_count: int = 0) -> InlineKeyboardMarkup:
    """
    Main Audio Menu
    """

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Merge Audio",
                    callback_data="audio_merge"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔄 Replace Audio",
                    callback_data="audio_replace"
                ),
                InlineKeyboardButton(
                    "❌ Remove Audio",
                    callback_data="audio_remove"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔀 Swap Audio",
                    callback_data="audio_swap"
                ),
                InlineKeyboardButton(
                    "⭐ Default Audio",
                    callback_data="audio_default"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏷 Rename Track",
                    callback_data="audio_rename"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎵 Extract Audio",
                    callback_data="audio_extract"
                ),
                InlineKeyboardButton(
                    "📋 Track Info",
                    callback_data="audio_tracks"
                )
            ],
            [
                InlineKeyboardButton(
                    f"📊 Audio Tracks ({audio_count})",
                    callback_data="ignore"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="menu_main"
                ),
                InlineKeyboardButton(
                    "🏠 Home",
                    callback_data="home"
                )
            ]
        ]
    )
