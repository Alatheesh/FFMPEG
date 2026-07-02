from __future__ import annotations

import asyncio
import os

from pyrogram import filters
from pyrogram.types import Message

from bot.client import app
from bot.keyboards import Keyboards
from bot.messages import Messages

from bot.workspace import workspace

from models.media_asset import MediaAsset
from models.asset_type import AssetType

from core.ffprobe import FFProbe

probe=FFProbe()

# ===========================================================
# Helpers
# ===========================================================

async def refresh_dashboard(user_id:int):

    ws=workspace.get(user_id)

    if ws is None:
        return

    dashboard=getattr(ws,"dashboard_message",None)

    if dashboard is None:
        return

    try:

        await dashboard.edit_text(
            Messages.home(ws),
            reply_markup=Keyboards.home()
        )

    except Exception:
        pass


async def create_dashboard(message:Message):

    ws=workspace.get(message.from_user.id)

    dashboard=await message.reply_text(
        Messages.home(ws),
        reply_markup=Keyboards.home()
    )

    ws.dashboard_message=dashboard


def create_asset(
    file_path,
    file_name,
    file_size
):

    asset=MediaAsset()

    asset.name=file_name
    asset.path=file_path
    asset.size=file_size
    asset.type=AssetType.VIDEO.value

    return asset


# ===========================================================
# Commands
# ===========================================================

@app.on_message(filters.command("start"))

async def start_handler(
    client,
    message:Message
):

    await message.reply_text(
        "👋 Welcome to Auto Media Editor.\n\n"
        "Send a video to begin.",
        reply_markup=Keyboards.home()
    )


@app.on_message(filters.command("help"))

async def help_handler(
    client,
    message:Message
):

    await message.reply_text(
        Messages.help()
    )


@app.on_message(filters.command("about"))

async def about_handler(
    client,
    message:Message
):

    await message.reply_text(
        Messages.about()
    )


@app.on_message(filters.command("cancel"))

async def cancel_handler(
    client,
    message:Message
):

    ws=workspace.get(message.from_user.id)

    if ws:

        ws.reset()

    await message.reply_text(
        "✅ Workspace cancelled."
    )


# ===========================================================
# Video Upload
# ===========================================================

@app.on_message(
    filters.video|
    filters.document
)

async def video_handler(
    client,
    message:Message
):

    media=message.video or message.document

    if media is None:
        return

    filename=media.file_name or ""

    extension=os.path.splitext(
        filename
    )[1].lower()

    if extension not in (
        ".mkv",
        ".mp4",
        ".avi",
        ".mov",
        ".webm",
        ".flv",
        ".m4v",
        ".ts",
        ".m2ts"
    ):

        return

    status=await message.reply_text(
        "📥 Downloading..."
    )

    download_path=await message.download()

    await status.edit_text(
        "🔍 Reading media information..."
    )

    metadata=await asyncio.to_thread(
        probe.probe,
        download_path
    )

    user_id=message.from_user.id

    ws=workspace.create(user_id)

    asset=create_asset(
        download_path,
        filename,
        media.file_size
    )

    asset.metadata=metadata

    ws.add_asset(asset)

    ws.set_main_video(asset)

    await status.delete()

    await create_dashboard(message)
# ===========================================================
# Upload Router
# ===========================================================

VIDEO_EXTENSIONS={
    ".mkv",".mp4",".avi",".mov",".webm",
    ".flv",".m4v",".ts",".m2ts"
}

AUDIO_EXTENSIONS={
    ".aac",".ac3",".eac3",".dts",".flac",
    ".mp3",".m4a",".opus",".ogg",".wav"
}

SUBTITLE_EXTENSIONS={
    ".srt",".ass",".ssa",".vtt",".sup",".sub"
}

IMAGE_EXTENSIONS={
    ".jpg",".jpeg",".png",".webp"
}

FONT_EXTENSIONS={
    ".ttf",".otf",".woff",".woff2"
}


def detect_file_type(filename:str):

    extension=os.path.splitext(
        filename
    )[1].lower()

    if extension in VIDEO_EXTENSIONS:
        return "video"

    if extension in AUDIO_EXTENSIONS:
        return "audio"

    if extension in SUBTITLE_EXTENSIONS:
        return "subtitle"

    if extension in IMAGE_EXTENSIONS:
        return "thumbnail"

    if extension in FONT_EXTENSIONS:
        return "font"

    return "unknown"


async def create_uploaded_asset(
    message:Message,
    asset_type:str
):

    media=(
        message.document
        or message.video
        or message.audio
        or message.photo
    )

    if media is None:
        return None

    path=await message.download()

    asset=MediaAsset()

    asset.name=getattr(
        media,
        "file_name",
        os.path.basename(path)
    )

    asset.path=path

    asset.size=getattr(
        media,
        "file_size",
        os.path.getsize(path)
    )

    asset.type=asset_type

    try:

        if asset_type in (
            "video",
            "audio"
        ):

            asset.metadata=await asyncio.to_thread(
                probe.probe,
                path
            )

    except Exception:

        asset.metadata={}

    return asset


# ===========================================================
# Pending Uploads
# ===========================================================

async def receive_audio(
    ws,
    message,
    asset
):

    ws.add_asset(asset)

    ws.audio_asset=asset

    ws.pending_action=None

    await refresh_dashboard(
        message.from_user.id
    )


async def receive_subtitle(
    ws,
    message,
    asset
):

    ws.add_asset(asset)

    ws.subtitle_asset=asset

    ws.pending_action=None

    await refresh_dashboard(
        message.from_user.id
    )


async def receive_thumbnail(
    ws,
    message,
    asset
):

    ws.add_asset(asset)

    ws.thumbnail_asset=asset

    ws.pending_action=None

    await refresh_dashboard(
        message.from_user.id
    )


async def receive_font(
    ws,
    message,
    asset
):

    ws.add_asset(asset)

    ws.fonts.append(asset)

    ws.pending_action=None

    await refresh_dashboard(
        message.from_user.id
    )


# ===========================================================
# Upload Dispatcher
# ===========================================================

@app.on_message(
    filters.document|
    filters.audio|
    filters.photo
)

async def upload_router(
    client,
    message:Message
):

    user_id=message.from_user.id

    ws=workspace.get(user_id)

    if ws is None:
        return

    media=(
        message.document
        or message.audio
        or message.photo
    )

    if media is None:
        return

    filename=getattr(
        media,
        "file_name",
        "image.jpg"
    )

    file_type=detect_file_type(
        filename
    )

    pending=getattr(
        ws,
        "pending_action",
        None
    )

    if pending is None:
        return

    status=await message.reply_text(
        "📥 Receiving file..."
    )

    asset=await create_uploaded_asset(
        message,
        file_type
    )

    if asset is None:

        await status.edit_text(
            "❌ Failed to receive file."
        )

        return

    if pending=="replace_audio":

        await receive_audio(
            ws,
            message,
            asset
        )

    elif pending=="replace_subtitle":

        await receive_subtitle(
            ws,
            message,
            asset
        )

    elif pending=="replace_thumbnail":

        await receive_thumbnail(
            ws,
            message,
            asset
        )

    elif pending=="upload_font":

        await receive_font(
            ws,
            message,
            asset
        )

    else:

        await status.edit_text(
            "❌ Unknown pending action."
        )

        return

    await status.edit_text(
        "✅ File added successfully."
    )

    await refresh_dashboard(
        user_id
    )
from pyrogram.types import CallbackQuery

# ===========================================================
# Callback Queries
# ===========================================================

@app.on_callback_query()
async def callback_handler(
    client,
    callback:CallbackQuery
):

    user_id=callback.from_user.id

    ws=workspace.get(user_id)

    if ws is None:

        await callback.answer(
            "Upload a video first.",
            show_alert=True
        )

        return

    data=callback.data or ""

    try:

        if data=="home":

            await callback.message.edit_text(
                Messages.home(ws),
                reply_markup=Keyboards.home()
            )

            return await callback.answer()

        # ===================================================
        # Main Menus
        # ===================================================

        if data=="menu:audio":

            await callback.message.edit_text(
                Messages.audio(ws),
                reply_markup=Keyboards.audio()
            )

            return await callback.answer()

        if data=="menu:subtitle":

            await callback.message.edit_text(
                Messages.subtitle(ws),
                reply_markup=Keyboards.subtitle()
            )

            return await callback.answer()

        if data=="menu:video":

            await callback.message.edit_text(
                Messages.video(ws),
                reply_markup=Keyboards.video()
            )

            return await callback.answer()

        if data=="menu:thumbnail":

            await callback.message.edit_text(
                Messages.thumbnail(ws),
                reply_markup=Keyboards.thumbnail()
            )

            return await callback.answer()

        if data=="menu:metadata":

            await callback.message.edit_text(
                Messages.metadata(ws),
                reply_markup=Keyboards.metadata()
            )

            return await callback.answer()

        if data=="menu:workspace":

            await callback.message.edit_text(
                Messages.workspace(ws),
                reply_markup=Keyboards.workspace()
            )

            return await callback.answer()

        if data=="menu:export":

            await callback.message.edit_text(
                Messages.export(ws),
                reply_markup=Keyboards.export()
            )

            return await callback.answer()

        if data=="menu:settings":

            await callback.message.edit_text(
                "⚙ Settings",
                reply_markup=Keyboards.settings()
            )

            return await callback.answer()

        # ===================================================
        # Audio Upload Requests
        # ===================================================

        if data=="audio:replace":

            ws.pending_action={
                "action":"replace_audio"
            }

            await callback.message.reply_text(
                "🎵 Send the new audio file."
            )

            return await callback.answer()

        if data=="subtitle:replace":

            ws.pending_action={
                "action":"replace_subtitle"
            }

            await callback.message.reply_text(
                "💬 Send the subtitle file."
            )

            return await callback.answer()

        if data=="thumbnail:replace":

            ws.pending_action={
                "action":"replace_thumbnail"
            }

            await callback.message.reply_text(
                "🖼 Send the thumbnail image."
            )

            return await callback.answer()

        if data=="workspace:clear":

            ws.reset()

            await callback.message.edit_text(
                Messages.empty_workspace(),
                reply_markup=Keyboards.home()
            )

            return await callback.answer(
                "Workspace cleared."
            )

        if data=="export:summary":

            await callback.message.edit_text(
                Messages.export(ws),
                reply_markup=Keyboards.export()
            )

            return await callback.answer()

        if data=="close":

            await callback.message.delete()

            return await callback.answer()

        # ===================================================
        # Dynamic Audio Track
        # ===================================================

        if data.startswith("audio:track:"):

            index=int(
                data.split(":")[-1]
            )

            ws.selected_audio=index

            await callback.answer(
                f"Selected audio track {index}"
            )

            return

        # ===================================================
        # Dynamic Subtitle Track
        # ===================================================

        if data.startswith("subtitle:track:"):

            index=int(
                data.split(":")[-1]
            )

            ws.selected_subtitle=index

            await callback.answer(
                f"Selected subtitle track {index}"
            )

            return

        # ===================================================
        # Queue Viewer
        # ===================================================

        if data.startswith("queue:view:"):

            operation_id=data.split(":")[-1]

            await callback.answer(
                f"Operation {operation_id}"
            )

            return

        await callback.answer(
            "Coming soon."
        )

    except Exception as e:

        await callback.answer(
            str(e),
            show_alert=True
        )
# ===========================================================
# Text Input Router
# ===========================================================

@app.on_message(
    filters.private&
    filters.text&
    ~filters.command([
        "start",
        "help",
        "about",
        "cancel"
    ])
)
async def text_router(
    client,
    message:Message
):

    user_id=message.from_user.id

    ws=workspace.get(user_id)

    if ws is None:
        return

    pending=getattr(
        ws,
        "pending_action",
        None
    )

    if not pending:
        return

    if isinstance(pending,dict):
        action=pending.get("action")
    else:
        action=pending

    text=message.text.strip()

    try:

        # ==============================================
        # Audio Rename
        # ==============================================

        if action=="rename_audio":

            stream=ws.selected_audio

            ws.audio_manager.rename(
                stream,
                text
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Audio renamed."
            )

            return

        # ==============================================
        # Subtitle Rename
        # ==============================================

        if action=="rename_subtitle":

            stream=ws.selected_subtitle

            ws.media_manager.rename_subtitle(
                stream,
                text
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Subtitle renamed."
            )

            return

        # ==============================================
        # Metadata
        # ==============================================

        if action=="metadata_title":

            ws.media_manager.set_title(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Title updated."
            )

            return

        if action=="metadata_author":

            ws.media_manager.set_author(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Author updated."
            )

            return

        if action=="metadata_description":

            ws.media_manager.set_description(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Description updated."
            )

            return

        if action=="metadata_comment":

            ws.media_manager.set_comment(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Comment updated."
            )

            return

        if action=="metadata_copyright":

            ws.media_manager.set_copyright(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Copyright updated."
            )

            return

        if action=="metadata_encoder":

            ws.media_manager.set_encoder(text)

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Encoder updated."
            )

            return

        # ==============================================
        # Language
        # ==============================================

        if action=="audio_language":

            stream=ws.selected_audio

            ws.audio_manager.set_language(
                stream,
                text
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Audio language updated."
            )

            return

        if action=="subtitle_language":

            stream=ws.selected_subtitle

            ws.media_manager.rename_subtitle(
                stream,
                text
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Subtitle language updated."
            )

            return

        # ==============================================
        # Video Trim
        # ==============================================

        if action=="video_trim":

            values=text.split()

            if len(values)!=2:

                await message.reply_text(
                    "Send:\n00:00:10 00:01:20"
                )

                return

            ws.media_manager.trim(
                values[0],
                values[1]
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Trim added."
            )

            return

        # ==============================================
        # Resize
        # ==============================================

        if action=="video_resize":

            values=text.lower().replace("x"," ").split()

            if len(values)!=2:

                await message.reply_text(
                    "Example:\n1920x1080"
                )

                return

            width=int(values[0])
            height=int(values[1])

            ws.media_manager.resize(
                width,
                height
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Resize added."
            )

            return

        # ==============================================
        # Rotate
        # ==============================================

        if action=="video_rotate":

            angle=int(text)

            ws.media_manager.rotate(
                angle
            )

            ws.pending_action=None

            await refresh_dashboard(user_id)

            await message.reply_text(
                "✅ Rotation added."
            )

            return

        await message.reply_text(
            "⚠ No handler for this input."
        )

    except Exception as e:

        await message.reply_text(
            f"❌ {e}"
        )
# ===========================================================
# Export
# ===========================================================

running_jobs={}


@app.on_callback_query(filters.regex("^export:start$"))
async def export_handler(
    client,
    callback:CallbackQuery
):

    user_id=callback.from_user.id

    ws=workspace.get(user_id)

    if ws is None:

        await callback.answer(
            "Workspace not found.",
            show_alert=True
        )

        return

    if user_id in running_jobs:

        await callback.answer(
            "Export already running.",
            show_alert=True
        )

        return

    async def progress(
        percent,
        status
    ):

        try:

            await ws.dashboard_message.edit_text(
                Messages.processing(
                    operation=status,
                    progress=percent
                ),
                reply_markup=Keyboards.processing()
            )

        except Exception:
            pass

    ws.media_engine.set_progress_callback(
        progress
    )

    task=asyncio.create_task(
        ws.media_engine.export()
    )

    running_jobs[user_id]=task

    await callback.answer(
        "Export started."
    )

    try:

        output_file=await task

        await ws.dashboard_message.edit_text(
            Messages.completed(
                filename=os.path.basename(output_file),
                elapsed="-",
                output_size=Messages._size(
                    os.path.getsize(output_file)
                )
            ),
            reply_markup=Keyboards.completed()
        )

        await client.send_document(
            chat_id=user_id,
            document=output_file,
            caption="✅ Export completed."
        )

    except asyncio.CancelledError:

        await ws.dashboard_message.edit_text(
            Messages.warning(
                "Export cancelled."
            ),
            reply_markup=Keyboards.home()
        )

    except Exception as e:

        await ws.dashboard_message.edit_text(
            Messages.error(str(e)),
            reply_markup=Keyboards.home()
        )

    finally:

        running_jobs.pop(
            user_id,
            None
        )


# ===========================================================
# Cancel Export
# ===========================================================

@app.on_callback_query(
    filters.regex("^export:cancel$")
)
async def cancel_export(
    client,
    callback:CallbackQuery
):

    user_id=callback.from_user.id

    task=running_jobs.get(user_id)

    ws=workspace.get(user_id)

    if task:

        task.cancel()

    if ws:

        try:
            ws.media_engine.cancel()
        except Exception:
            pass

    await callback.answer(
        "Cancelling..."
    )


# ===========================================================
# Download Button
# ===========================================================

@app.on_callback_query(
    filters.regex("^export:download$")
)
async def download_again(
    client,
    callback:CallbackQuery
):

    ws=workspace.get(
        callback.from_user.id
    )

    if ws is None:
        return

    output=getattr(
        ws,
        "last_output",
        None
    )

    if output and os.path.exists(output):

        await client.send_document(
            callback.message.chat.id,
            output
        )

    else:

        await callback.answer(
            "Output not found.",
            show_alert=True
        )


# ===========================================================
# Workspace Cleanup
# ===========================================================

async def cleanup_workspace(
    user_id:int
):

    ws=workspace.get(user_id)

    if ws is None:
        return

    try:

        ws.media_engine.cleanup()

    except Exception:
        pass

    workspace.remove(user_id)


# ===========================================================
# Startup Recovery
# ===========================================================

async def recover_jobs():

    if "database" not in globals():
        return

    try:

        jobs=await database.recover_jobs()

        for job in jobs:

            print(
                f"Recovering job "
                f"{job['job_id']}"
            )

    except Exception as e:

        print(e)


# ===========================================================
# Shutdown
# ===========================================================

async def shutdown():

    for user_id in list(running_jobs):

        task=running_jobs[user_id]

        task.cancel()

    for user_id in list(workspace.keys()):

        await cleanup_workspace(user_id)
