import os
import logging
import asyncio
from pyrogram import Client
from pyrogram.types import Message
from database import save_workspace
from config import Config
from engine.ffmpeg import compile_ffmpeg_command, execute_ffmpeg
from storage.telegram import TelegramStorageProvider
from storage.b2 import B2StorageProvider
from storage.local import LocalStorageProvider

logger = logging.getLogger(__name__)

async def run_export(client: Client, message: Message, workspace):
    user_id = workspace.user_id
    
    # 1. Verification
    if not workspace.main_video_id or workspace.main_video_id not in workspace.assets:
        await message.reply_text("❌ No video file in workspace. Please upload one first.")
        return
        
    main_video = workspace.assets[workspace.main_video_id]
    duration = main_video.metadata.get("duration", 0.0)
    
    # 2. Output Configurations
    ext = workspace.output_settings.get("format", "mkv")
    output_filename = f"edited_{user_id}_{int(asyncio.get_event_loop().time())}.{ext}"
    output_path = os.path.join(Config.OUTPUTS_DIR, output_filename)
    
    status_msg = await message.reply_text("🚀 **Initializing rendering engine...**")
    
    try:
        # Compile Command
        cmd = compile_ffmpeg_command(workspace, output_path)
        logger.info(f"Generated FFmpeg Command for user {user_id}: {cmd}")
        
        last_percent = -1
        
        # 3. Dynamic Progress Bar Callback
        async def progress_callback(percent):
            nonlocal last_percent
            if percent - last_percent >= 5 or percent == 100:
                last_percent = percent
                bar_filled = percent // 5
                bar = "█" * bar_filled + "░" * (20 - bar_filled)
                try:
                    await status_msg.edit_text(
                        f"🎬 **Rendering Video Operations...**\n\n"
                        f"`[{bar}] {percent}%`\n\n"
                        f"⚠️ _This might take a few minutes depending on operations (encoding vs copying)._"
                    )
                except Exception:
                    pass  # Prevent crash on edit failures
                    
        # 4. Execute FFmpeg
        success = await execute_ffmpeg(cmd, duration, progress_callback)
        
        if not success or not os.path.exists(output_path):
            await status_msg.edit_text("❌ **Rendering Failed!** Check log files for issues with codecs/compatibility.")
            return
            
        await status_msg.edit_text("📤 **Processing Complete! Uploading to storage...**")
        
        # 5. Storage Upload and Delivery
        b2_link = None
        if Config.B2_ENABLED:
            try:
                await status_msg.edit_text("📤 **Processing Complete! Uploading to Backblaze B2...**")
                b2_provider = B2StorageProvider()
                # Run upload in thread to avoid blocking Pyrogram
                b2_link = await b2_provider.upload_file(output_path, output_filename)
            except Exception as e:
                logger.error(f"Failed to upload to Backblaze B2: {e}")
                
        await status_msg.edit_text("📤 **Uploading file to Telegram...**")
        
        tg_provider = TelegramStorageProvider(client)
        # Uploads file and delivers to user's chat
        await tg_provider.upload_file(
            local_path=output_path,
            filename=output_filename,
            chat_id=user_id
        )
        
        # Caption notes
        notes = "✅ **Export Completed Successfully!**\n\n"
        if b2_link:
            notes += f"🌐 **Backblaze B2 Permanent Link:**\n[Download File]({b2_link})\n\n"
        notes += "🧹 _Workspace temporary files cleaned._"
        
        await status_msg.delete()
        await client.send_message(chat_id=user_id, text=notes, disable_web_page_preview=True)
        
        # 6. Cleanup files locally
        await cleanup_workspace_files(workspace)
        
        # Reset pipeline state
        workspace.pipeline.clear()
        workspace.main_video_id = None
        workspace.assets.clear()
        workspace.dashboard_message_id = None
        workspace.pending_action = None
        await save_workspace(workspace)
        
    except Exception as e:
        logger.error(f"Error during export: {e}")
        try:
            await status_msg.edit_text(f"❌ **Export Process Interrupted:** `{e}`")
        except Exception:
            pass

async def cleanup_workspace_files(workspace):
    """
    Deletes all temporary files (inputs, downloads, outputs) associated with the workspace assets.
    """
    local_provider = LocalStorageProvider()
    for asset in workspace.assets.values():
        if os.path.exists(asset.file_path):
            await local_provider.delete_file(asset.file_path)
            
    # Also scan temp directories for any residue files containing the user ID
    try:
        for folder in [Config.DOWNLOADS_DIR, Config.OUTPUTS_DIR]:
            if not os.path.exists(folder):
                continue
            for file in os.listdir(folder):
                if file.startswith(f"edited_{workspace.user_id}") or file.startswith(str(workspace.user_id)):
                    full_path = os.path.join(folder, file)
                    if os.path.exists(full_path):
                        os.remove(full_path)
    except Exception as e:
        logger.error(f"Error during workspace files cleanup: {e}")
