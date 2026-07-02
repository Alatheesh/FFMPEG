from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ExportScreen:

    @staticmethod
    def build(workspace):

        asset = workspace.get_main_video()

        filename = "Unknown"

        if asset:
            filename = asset.name

        pending = len(workspace.pending_operations)

        output = workspace.output

        container = output.get("container") or "Keep Original"

        text = (
            "📦 **Export Settings**\n\n"
            f"🎬 File : `{filename}`\n"
            f"🛠 Pending Changes : `{pending}`\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            f"📁 Container : `{container}`\n"
            "🎥 Video Codec : `Copy`\n"
            "🎵 Audio Codec : `Copy`\n"
            "💬 Subtitle : `Copy`\n"
            "🖼 Thumbnail : `Keep`\n"
            "📝 Metadata : `Keep`\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "Select what you want to configure."
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 Container",
                        callback_data="export:container"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎥 Video",
                        callback_data="export:video"
                    ),
                    InlineKeyboardButton(
                        "🎵 Audio",
                        callback_data="export:audio"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 Subtitle",
                        callback_data="export:subtitle"
                    ),
                    InlineKeyboardButton(
                        "🖼 Thumbnail",
                        callback_data="export:thumbnail"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 Metadata",
                        callback_data="export:metadata"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🚀 Export Video",
                        callback_data="workspace:export"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home:open"
                    )
                ]
            ]
        )

        return {
            "text": text,
            "reply_markup": keyboard
        }
