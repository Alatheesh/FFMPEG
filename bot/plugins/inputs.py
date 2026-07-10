import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import get_workspace, save_workspace
from engine.ffprobe import run_ffprobe
from bot.dashboard import render_dashboard
from config import Config

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.video | filters.document | filters.audio | filters.photo | filters.text))
async def inputs_handler(client: Client, message: Message):
    user_id = message.from_user.id
    workspace = await get_workspace(user_id)
    
    # 1. Initialize Main Video
    # If the user sends a video and there is no main video active in workspace
    if (message.video or (message.document and message.document.mime_type and "video" in message.document.mime_type)) and not workspace.main_video_id:
        loading = await message.reply_text("📥 **Downloading main video, please wait...**")
        
        file_obj = message.video if message.video else message.document
        filename = file_obj.file_name or "video.mp4"
        dest_path = os.path.join(Config.DOWNLOADS_DIR, f"{user_id}_main_{filename}")
        
        try:
            # Download file locally
            local_path = await client.download_media(message, file_name=dest_path)
            
            # Analyze using ffprobe
            loading2 = await loading.edit_text("🔍 **Analyzing video structure (FFprobe)...**")
            meta = await run_ffprobe(local_path)
            
            if not meta:
                await loading2.edit_text("❌ Failed to parse media metadata. Ensure the file is not corrupted.")
                # Cleanup
                if os.path.exists(local_path):
                    os.remove(local_path)
                return
                
            # Create main asset
            workspace.add_asset(
                file_path=local_path,
                file_size=file_obj.file_size,
                file_type="video",
                metadata=meta
            )
            workspace.add_history(f"Initialized workspace with video: {filename}")
            await save_workspace(workspace)
            
            await loading2.delete()
            
            # Render and send Dashboard Console
            text, keyboard = render_dashboard(workspace)
            msg = await message.reply_text(text, reply_markup=keyboard)
            
            workspace.dashboard_message_id = msg.id
            await save_workspace(workspace)
            return
            
        except Exception as e:
            logger.error(f"Failed to initialize video: {e}")
            await loading.edit_text(f"❌ Failed to download and initialize video: `{e}`")
            return

    # If workspace is not initialized and they send other inputs, guide them
    if not workspace.main_video_id:
        await message.reply_text("👋 **Auto Media Editor**\n\nPlease upload a video file to initialize your workspace console first.")
        return

    # 2. Process Pending Action Inputs
    pending = workspace.pending_action
    if not pending:
        # Ignore random messages if no action is pending
        return
        
    # --- File Upload Action Handling ---
    if pending in ["replace_audio", "add_audio"]:
        if not message.audio and not (message.document and message.document.mime_type and "audio" in message.document.mime_type):
            await message.reply_text("❌ Please upload a valid audio file (e.g. MP3, M4A).")
            return
            
        loading = await message.reply_text("📥 Downloading audio track...")
        file_obj = message.audio if message.audio else message.document
        filename = file_obj.file_name or "audio.mp3"
        dest_path = os.path.join(Config.DOWNLOADS_DIR, f"{user_id}_audio_{filename}")
        
        try:
            local_path = await client.download_media(message, file_name=dest_path)
            asset = workspace.add_asset(local_path, file_obj.file_size, "audio")
            
            if pending == "add_audio":
                workspace.add_operation("add_audio", {
                    "asset_id": asset.id,
                    "title": filename.split(".")[0],
                    "language": "und",
                    "default": False
                })
                workspace.pending_action = None
                await save_workspace(workspace)
                await loading.edit_text("✅ Audio track added to operation pipeline!")
                await update_dashboard(client, workspace)
            else:
                # Transition to index prompt
                workspace.pending_action = f"replace_audio_idx#{asset.id}#{filename}"
                await save_workspace(workspace)
                await loading.edit_text(
                    "📥 Audio downloaded.\n\n"
                    "Now send me the **track index** inside the video to replace (e.g. type `0` to replace the first audio track)."
                )
        except Exception as e:
            await loading.edit_text(f"❌ Failed: `{e}`")
            
    elif pending == "add_sub":
        if not message.document or not (message.document.file_name.endswith((".srt", ".ass"))):
            await message.reply_text("❌ Please upload a valid subtitle file (.srt or .ass).")
            return
            
        loading = await message.reply_text("📥 Downloading subtitle track...")
        filename = message.document.file_name
        dest_path = os.path.join(Config.DOWNLOADS_DIR, f"{user_id}_sub_{filename}")
        
        try:
            local_path = await client.download_media(message, file_name=dest_path)
            asset = workspace.add_asset(local_path, message.document.file_size, "subtitle")
            
            workspace.add_operation("add_subtitle", {
                "asset_id": asset.id,
                "title": filename.split(".")[0],
                "language": "und",
                "default": False
            })
            workspace.pending_action = None
            await save_workspace(workspace)
            await loading.edit_text("✅ Subtitle track added to operation pipeline!")
            await update_dashboard(client, workspace)
        except Exception as e:
            await loading.edit_text(f"❌ Failed: `{e}`")
            
    elif pending == "add_thumb":
        if not message.photo and not (message.document and message.document.mime_type and "image" in message.document.mime_type):
            await message.reply_text("❌ Please upload a valid cover image.")
            return
            
        loading = await message.reply_text("📥 Downloading thumbnail cover...")
        dest_path = os.path.join(Config.DOWNLOADS_DIR, f"{user_id}_thumb_cover.jpg")
        
        try:
            local_path = await client.download_media(message, file_name=dest_path)
            asset = workspace.add_asset(local_path, 1000, "thumbnail") # Size is minor
            
            workspace.add_operation("add_thumbnail", {
                "asset_id": asset.id
            })
            workspace.pending_action = None
            await save_workspace(workspace)
            await loading.edit_text("✅ Thumbnail cover added to operation pipeline!")
            await update_dashboard(client, workspace)
        except Exception as e:
            await loading.edit_text(f"❌ Failed: `{e}`")

    # --- Text Input Action Handling ---
    elif message.text:
        text = message.text.strip()
        
        if pending.startswith("replace_audio_idx"):
            parts = pending.split("#")
            asset_id = parts[1]
            filename = parts[2]
            
            if not text.isdigit():
                await message.reply_text("❌ Please send a valid numeric index (e.g. `0`).")
                return
                
            track_idx = int(text)
            workspace.add_operation("replace_audio", {
                "asset_id": asset_id,
                "track_index": track_idx,
                "title": filename.split(".")[0],
                "language": "und"
            })
            workspace.pending_action = None
            await save_workspace(workspace)
            await message.reply_text(f"✅ Replaced Audio Track {track_idx} in pipeline!")
            await update_dashboard(client, workspace)
            
        elif pending == "edit_title":
            workspace.add_operation("set_metadata", {"title": text})
            workspace.pending_action = None
            await save_workspace(workspace)
            await message.reply_text("✅ Video Title metadata updated in pipeline!")
            await update_dashboard(client, workspace)
            
        elif pending == "edit_artist":
            workspace.add_operation("set_metadata", {"artist": text})
            workspace.pending_action = None
            await save_workspace(workspace)
            await message.reply_text("✅ Artist metadata updated in pipeline!")
            await update_dashboard(client, workspace)
            
        elif pending == "trim":
            # Parse start:end coordinates
            match = re.match(r"^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$", text)
            if not match:
                await message.reply_text("❌ Formatting error. Use `START:END` in seconds (e.g. `10.5:60`).")
                return
                
            start = float(match.group(1))
            end = float(match.group(2))
            
            # Quick range check against duration
            video_asset = workspace.assets[workspace.main_video_id]
            dur = video_asset.metadata.get("duration", 0.0)
            
            if start >= end or (dur > 0 and end > dur):
                await message.reply_text(f"❌ Limits error. Start must be less than end, and end must fit inside duration ({dur}s).")
                return
                
            workspace.add_operation("trim_video", {"start": start, "end": end})
            workspace.pending_action = None
            await save_workspace(workspace)
            await message.reply_text("✅ Video trim range added to operation pipeline!")
            await update_dashboard(client, workspace)

import re

async def update_dashboard(client: Client, workspace: Workspace):
    if not workspace.dashboard_message_id:
        return
    text, keyboard = render_dashboard(workspace)
    try:
        await client.edit_message_text(
            chat_id=workspace.user_id,
            message_id=workspace.dashboard_message_id,
            text=text,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Failed to update dashboard message: {e}")
