import os
from pyrogram import Client
from storage.base import StorageProvider

class TelegramStorage(StorageProvider):
    """Uses Telegram chats as unlimited cloud storage."""
    
    def __init__(self, client: Client, default_chat_id: int):
        self.client = client
        self.default_chat_id = default_chat_id

    async def upload(self, file_path: str, caption: str = "Exported by Auto Media Editor") -> str:
        """Uploads the processed file directly back to the user."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot upload missing file: {file_path}")
            
        message = await self.client.send_document(
            chat_id=self.default_chat_id,
            document=file_path,
            caption=caption,
            force_document=True 
        )
        # Return the message ID as the reference for this file
        return str(message.id)

    async def download(self, pyrogram_message, destination_path: str) -> str:
        """Downloads a file from a Telegram message."""
        file_path = await self.client.download_media(
            message=pyrogram_message,
            file_name=destination_path
        )
        return file_path
