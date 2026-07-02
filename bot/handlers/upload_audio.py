import os
import uuid

from pyrogram import filters
from pyrogram.types import Message

from bot.client import app
from bot.workspace import workspace
from constants import (
    WorkspaceState,
    AssetType
)
from config import DOWNLOAD_DIR
from core.ffprobe import probe
from models.media_asset import MediaAsset


# Supported audio extensions
SUPPORTED_AUDIO = (
    ".aac",
    ".ac3",
    ".eac3",
    ".mp3",
    ".m4a",
    ".flac",
    ".wav",
    ".opus",
    ".ogg",
    ".dts",
    ".truehd"
)


@app.on_message(filters.audio | filters.document)
async def receive_audio(client, message: Message):

    user_id = message.from_user.id

    ws = workspace.get(user_id)

    if ws is None:
        return

    # Accept audio only if we're waiting for it
    if ws.state != WorkspaceState.WAITING_AUDIO:
        return

    media = message.audio or message.document

    if media is None:
        return

    filename = getattr(media, "file_name", "")

    if not filename.lower().endswith(SUPPORTED_AUDIO):

        await message.reply_text(
            "❌ Unsupported audio format."
        )

        return

    unique_name = (
        f"{uuid.uuid4()}_{filename}"
    )

    file_path = os.path.join(
        DOWNLOAD_DIR,
        unique_name
    )

    status = await message.reply_text(
        "⬇ Downloading audio..."
    )

    await message.download(
        file_name=file_path
    )

    info = probe(file_path)

    asset = MediaAsset()

    asset.name = filename
    asset.path = file_path
    asset.type = AssetType.AUDIO.value
    asset.size = media.file_size

    asset.format = (
        info.get("format", {})
        .get("format_name", "")
    )

    asset.metadata = info

    for stream in info.get("streams", []):

        codec_type = stream.get("codec_type")

        if codec_type == "audio":
            asset.audio_streams.append(stream)

    asset_id = ws.assets.add(asset)

    await status.edit_text(
        "✅ Audio uploaded successfully.\n\n"
        f"📁 {asset.name}\n"
        f"🆔 Asset ID: `{asset_id}`\n\n"
        "Continue editing your workspace."
    )
