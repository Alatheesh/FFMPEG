from pyrogram import filters
from pyrogram.types import Message

from bot.client import app


@app.on_message(filters.command("start"))
async def start_command(client, message: Message):

    text = (
        "🎬 **Telegram Media Editor**\n\n"
        "Welcome!\n\n"
        "📤 Send me any video file to begin.\n\n"
        "Supported formats:\n"
        "• MKV\n"
        "• MP4\n"
        "• AVI\n"
        "• MOV\n"
        "• WEBM\n"
        "• TS\n"
        "• FLV\n"
        "• M4V\n"
        "• And most formats supported by FFmpeg.\n\n"
        "After you send a video, I'll analyze it and let you choose what you'd like to do."
    )

    await message.reply_text(text)
