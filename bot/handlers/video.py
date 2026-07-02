import os
import uuid

from pyrogram import filters
from pyrogram.types import Message

from bot.client import app
from bot.workspace import workspace
from bot.keyboards.main import main_menu
from config import DOWNLOAD_DIR


# Accept videos sent as Telegram videos or documents
VIDEO_FILTER = (
    filters.video |
    filters.document
)


@app.on_message(VIDEO_FILTER)
async def receive_video(client, message: Message):

    user_id = message.from_user.id

    # Create a fresh workspace
    workspace.create(user_id)

    await message.reply_text(
        "📥 Receiving your media...\n"
        "Please wait."
    )

    media = message.video or message.document

    if not media:
        return

    # Original filename
    filename = getattr(media, "file_name", None)

    if not filename:
        filename = f"{uuid.uuid4()}.mkv"

    # Create unique filename
    unique_name = f"{uuid.uuid4()}_{filename}"

    file_path = os.path.join(
        DOWNLOAD_DIR,
        unique_name
    )

    # Download the file
    await message.download(
        file_name=file_path
    )

    # Save into workspace
    data = workspace.get(user_id)

    data["video"] = {
        "path": file_path,
        "name": filename,
        "size": media.file_size
    }

    await message.reply_text(
        f"✅ **{filename}** received successfully.\n\n"
        "🔍 Media analysis will be added in the next step.\n\n"
        "Choose what you want to do:",
        reply_markup=main_menu()
    )
