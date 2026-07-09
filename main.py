import os
import uuid
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from core.workspace import WorkspaceManager, MediaAsset, Operation
from core.pipeline import FFmpegCompiler

API_ID = int(os.environ.get("TELEGRAM_API_ID", "27725592"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "251ee09a3651d97f5fea5d0a2b7154b6")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6259120295:AAEbXCLsD_9PRUpblGrC7E6j40pTqsRpAyY")

bot = Client("media_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
manager = WorkspaceManager()
TEMP_DIR = "/app/temp"

def generate_dashboard_markup(workspace) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 Audio Track", callback_data="mod_audio"),
            InlineKeyboardButton("📝 Subtitles", callback_data="mod_subs")
        ],
        [
            InlineKeyboardButton("🖼️ Thumbnail", callback_data="mod_thumb"),
            InlineKeyboardButton("🏷️ Edit Metadata", callback_data="mod_meta")
        ],
        [
            InlineKeyboardButton("🔄 Undo", callback_data="pipe_undo"),
            InlineKeyboardButton("🚀 Export Final Media", callback_data="pipe_export")
        ]
    ])

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    workspace = manager.get_workspace(message.from_user.id)
    await message.reply_text(
        f"Hello {message.from_user.first_name}, welcome to Auto Media Editor.\n"
        "Please send or forward any main video file to initialize an editing workspace session."
    )

@bot.on_message(filters.video & filters.private)
async def handle_video_upload(client: Client, message: Message):
    user_id = message.from_user.id
    workspace = manager.get_workspace(user_id)
    
    status_msg = await message.reply_text("📥 Downloading video structure context...")
    
    # Simulate saving metadata information safely
    asset_id = str(uuid.uuid4())
    mock_path = os.path.join(TEMP_DIR, "downloads", f"{asset_id}.mp4")
    
    asset = MediaAsset(
        asset_id=asset_id,
        file_path=mock_path,
        file_size=message.video.file_size,
        asset_type="video",
        duration=message.video.duration
    )
    workspace.assets[asset_id] = asset
    workspace.history.append("Initialized Workspace Video Stream Source")
    
    # Construct persistent unified console layout
    dash_text = (
        f"⚙️ **Media Workspace Dashboard**\n\n"
        f"📦 **Source Asset File Size:** {asset.file_size / (1024*1024):.2f} MB\n"
        f"⏱️ **Duration:** {asset.duration} seconds\n"
        f"📋 **Queued Actions Pipeline:** {len(workspace.pipeline)} operations\n"
    )
    
    dash = await message.reply_text(dash_text, reply_markup=generate_dashboard_markup(workspace))
    workspace.dashboard_message_id = dash.id
    await status_msg.delete()

@bot.on_callback_query()
async def handle_dashboard_navigation(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    workspace = manager.get_workspace(user_id)
    data = callback_query.data

    if data == "mod_meta":
        workspace.pending_action = "wait_meta_title"
        await callback_query.message.reply_text("⌨️ Reply directly with the text string to update the structural Title global track metadata tag:")
        await callback_query.answer()
        
    elif data == "pipe_undo":
        if workspace.pipeline:
            removed_op = workspace.pipeline.pop()
            workspace.history.append(f"Undo action: {removed_op.action}")
            await callback_query.answer("Undo operation successfully cleared.")
        else:
            await callback_query.answer("Pipeline queue is empty.", show_alert=True)
            
    elif data == "pipe_export":
        if not workspace.assets:
            await callback_query.answer("Error: Context holds no active streams.", show_alert=True)
            return
        
        await callback_query.message.reply_text("🚧 Constructing compilation execution pipeline blocks...")
        try:
            cmd = FFmpegCompiler.compile(workspace, os.path.join(TEMP_DIR, "outputs"))
            await callback_query.message.reply_text(f"🎬 **Generated Execution Command Array:**\n`{' '.join(cmd)}`")
        except Exception as e:
            await callback_query.message.reply_text(f"❌ Failed layout compilation pipeline calculation: {str(e)}")
        await callback_query.answer()

@bot.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def handle_text_inputs(client: Client, message: Message):
    user_id = message.from_user.id
    workspace = manager.get_workspace(user_id)
    
    if workspace.pending_action == "wait_meta_title":
        new_title = message.text
        op = Operation(op_id=str(uuid.uuid4()), module="metadata", action="set_title", parameters={"title": new_title})
        workspace.pipeline.append(op)
        workspace.history.append(f"Queued Title Update target: {new_title}")
        workspace.pending_action = None
        await message.reply_text(f"✅ Structural pipeline appended: Change video title to '{new_title}'. View dashboard targets to process.")

if __name__ == "__main__":
    bot.run()
