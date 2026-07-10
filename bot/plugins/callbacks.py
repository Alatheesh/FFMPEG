import logging
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from database import get_workspace, save_workspace
from bot.dashboard import render_dashboard

logger = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex(r"^(menu|action)#"))
async def callback_router(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    workspace = await get_workspace(user_id)
    
    data = query.data
    parts = data.split("#")
    prefix = parts[0]
    subdata = parts[1]
    
    # 1. Menu Routing
    if prefix == "menu":
        text, keyboard = render_dashboard(workspace, menu_name=subdata)
        try:
            await query.message.edit_text(text, reply_markup=keyboard)
        except Exception:
            pass
        await query.answer()
        return
        
    # 2. Action Routing
    if prefix == "action":
        action_parts = subdata.split("#")
        action_name = action_parts[0]
        
        if action_name == "undo":
            if workspace.pipeline:
                removed_op = workspace.pipeline.pop()
                workspace.add_history(f"Undid operation: {removed_op.op_type}")
                await save_workspace(workspace)
                await query.answer("Reverted last queued operation ↩️")
            else:
                await query.answer("No operations to undo! ❌", show_alert=True)
                
            text, keyboard = render_dashboard(workspace)
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "clear":
            if workspace.pipeline:
                workspace.pipeline.clear()
                workspace.add_history("Cleared operations pipeline")
                await save_workspace(workspace)
                await query.answer("Operations pipeline cleared 🗑️")
            else:
                await query.answer("Pipeline is already empty! ❌")
                
            text, keyboard = render_dashboard(workspace)
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "toggle_format":
            target_fmt = action_parts[1]
            workspace.output_settings["format"] = target_fmt
            workspace.add_history(f"Changed target format to {target_fmt.upper()}")
            await save_workspace(workspace)
            await query.answer(f"Changed output format to {target_fmt.upper()} ⚙️")
            
            text, keyboard = render_dashboard(workspace, menu_name="settings")
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "compress":
            preset = action_parts[1]
            workspace.add_operation("compress_video", {"preset": preset})
            await save_workspace(workspace)
            await query.answer(f"Queued video compression ({preset}) 🗜️")
            
            text, keyboard = render_dashboard(workspace, menu_name="video")
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "remove_audio":
            track_idx = int(action_parts[1])
            workspace.add_operation("remove_audio", {"track_index": track_idx})
            await save_workspace(workspace)
            await query.answer(f"Queued removal of audio track {track_idx} ❌")
            
            text, keyboard = render_dashboard(workspace, menu_name="audio")
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "remove_sub":
            track_idx = int(action_parts[1])
            workspace.add_operation("remove_subtitle", {"track_index": track_idx})
            await save_workspace(workspace)
            await query.answer(f"Queued removal of subtitle track {track_idx} ❌")
            
            text, keyboard = render_dashboard(workspace, menu_name="subtitle")
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "burn_sub":
            track_idx = int(action_parts[1])
            workspace.add_operation("burn_subtitle", {"track_index": track_idx})
            await save_workspace(workspace)
            await query.answer(f"Queued subtitle burn-in for track {track_idx} 🔥")
            
            text, keyboard = render_dashboard(workspace, menu_name="subtitle")
            await query.message.edit_text(text, reply_markup=keyboard)
            
        elif action_name == "prompt":
            prompt_target = action_parts[1]
            workspace.pending_action = prompt_target
            await save_workspace(workspace)
            
            instruction = ""
            if prompt_target == "replace_audio":
                instruction = "🎙️ **Replace Audio Action**\n\nUpload an audio file (MP3, M4A, etc.) to replace stream. I will prompt you for the target index next."
            elif prompt_target == "add_audio":
                instruction = "🎙️ **Add Audio Action**\n\nUpload an audio file (MP3, M4A, etc.) to add it as an extra track."
            elif prompt_target == "add_sub":
                instruction = "📝 **Add Subtitle Action**\n\nUpload a subtitle file (SRT or ASS format) to embed in the media."
            elif prompt_target == "add_thumb":
                instruction = "🎨 **Cover Art Action**\n\nUpload a photo to be used as video thumbnail art."
            elif prompt_target == "edit_title":
                instruction = "📝 **Edit Title Action**\n\nSend me the text for the global title metadata tag."
            elif prompt_target == "edit_artist":
                instruction = "🎤 **Edit Artist Action**\n\nSend me the text for the artist/author metadata tag."
            elif prompt_target == "trim":
                instruction = "✂️ **Trim Video Action**\n\nSend trim timestamps formatted as `START_SECONDS:END_SECONDS` (e.g. `10:45` to trim between 10 seconds and 45 seconds)."
                
            await query.message.reply_text(instruction)
            await query.answer()
            
        elif action_name == "export":
            # Delegate trigger to export handler
            # In Pyrogram we can fetch plugins or just run it via callback
            await query.answer("Initializing render queue...")
            from bot.plugins.export import run_export
            await run_export(client, query.message, workspace)
