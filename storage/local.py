import os
import shutil
import logging
from storage.base import StorageProvider
from config import Config

logger = logging.getLogger(__name__)

class LocalStorageProvider(StorageProvider):
    
    def __init__(self):
        self.downloads_dir = Config.DOWNLOADS_DIR
        self.outputs_dir = Config.OUTPUTS_DIR

    async def upload_file(self, local_path: str, filename: str) -> str:
        # For local storage, we can copy the file to outputs_dir
        dest = os.path.join(self.outputs_dir, filename)
        if os.path.abspath(local_path) != os.path.abspath(dest):
            # Run in executor to avoid blocking the event loop
            import asyncio
            await asyncio.to_thread(shutil.copy2, local_path, dest)
        return dest

    async def download_file(self, file_identifier: str, local_destination: str) -> str:
        if os.path.exists(file_identifier):
            if os.path.abspath(file_identifier) != os.path.abspath(local_destination):
                import asyncio
                await asyncio.to_thread(shutil.copy2, file_identifier, local_destination)
            return local_destination
        raise FileNotFoundError(f"Local file not found: {file_identifier}")

    async def delete_file(self, file_identifier: str) -> bool:
        try:
            if os.path.exists(file_identifier):
                os.remove(file_identifier)
                return True
        except Exception as e:
            logger.error(f"Error deleting local file {file_identifier}: {e}")
        return False
