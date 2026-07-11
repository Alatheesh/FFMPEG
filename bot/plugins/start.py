import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import get_workspace, save_workspace
from bot.dashboard import render_dashboard

logger = logging.getLogger(__name__)

# Added group=-1 so this handler runs before the inputs_handler
@Client.on_message(filters.command("start") & filters.private, group=-1)
async def start_command_handler(client: Client, message: Message):
    if not message.from_user:
        return
        
    user_id = message.from_user.id
    logger.info(f"Received /start command from user ID: {user_id}")
    workspace = await get_workspace(user_id)
    
    # Reset dashboard state if starting fresh
    workspace.dashboard_message_id = None
    await save_workspace(workspace)
    
    text, keyboard = render_dashboard(workspace)
    msg = await message.reply_text(text, reply_markup=keyboard)
    
    # Save dashboard message ID to update it dynamically later
    workspace.dashboard_message_id = msg.id
    await save_workspace(workspace)
