import logging
from pyrogram import Client
from storage.base import StorageProvider

logger = logging.getLogger(__name__)

class TelegramStorageProvider(StorageProvider):
    
    def __init__(self, client: Client):
        self.client = client

    async def upload_file(self, local_path: str, filename: str, chat_id: int = None) -> str:
        """
        Uploads local file to Telegram. If chat_id is provided, sends to that chat.
        Returns the Telegram file_id.
        """
        if not chat_id:
            raise ValueError("Telegram storage upload requires a valid chat_id destination.")
            
        logger.info(f"Uploading file '{filename}' from '{local_path}' to chat {chat_id}...")
        
        # Determine appropriate send method based on file extension
        ext = filename.lower().split(".")[-1]
        
        try:
            if ext in ["mp4", "mkv", "webm", "mov"]:
                msg = await self.client.send_video(
                    chat_id=chat_id,
                    video=local_path,
                    file_name=filename,
                    supports_streaming=True
                )
                file_id = msg.video.file_id
            elif ext in ["mp3", "m4a", "ogg", "wav"]:
                msg = await self.client.send_audio(
                    chat_id=chat_id,
                    audio=local_path,
                    file_name=filename
                )
                file_id = msg.audio.file_id
            elif ext in ["jpg", "jpeg", "png"]:
                msg = await self.client.send_photo(
                    chat_id=chat_id,
                    photo=local_path
                )
                file_id = msg.photo.file_id
            else:
                msg = await self.client.send_document(
                    chat_id=chat_id,
                    document=local_path,
                    file_name=filename
                )
                file_id = msg.document.file_id
                
            logger.info(f"Telegram upload complete. File ID: {file_id}")
            return file_id
            
        except Exception as e:
            logger.error(f"Error uploading file to Telegram: {e}")
            raise e

    async def download_file(self, file_identifier: str, local_destination: str) -> str:
        """
        Downloads a Telegram file_id to local destination.
        """
        logger.info(f"Downloading Telegram file ID: {file_identifier} to {local_destination}...")
        try:
            path = await self.client.download_media(
                message=file_identifier,
                file_name=local_destination
            )
            logger.info(f"Telegram download complete: {path}")
            return path
        except Exception as e:
            logger.error(f"Error downloading file from Telegram: {e}")
            raise e

    async def delete_file(self, file_identifier: str) -> bool:
        # Telegram API does not support deleting files from their servers directly via file_id.
        # Files are automatically deleted if the message is deleted, but we only have file_id here.
        # Return True since it's a no-op on Telegram servers without message deletion.
        return True
