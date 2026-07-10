import logging
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from storage.base import StorageProvider
from config import Config

logger = logging.getLogger(__name__)

class B2StorageProvider(StorageProvider):
    def __init__(self):
        self.key_id = Config.B2_KEY_ID
        self.application_key = Config.B2_APPLICATION_KEY
        self.bucket_name = Config.B2_BUCKET_NAME
        self.api = None
        self.bucket = None
        
    def _init_b2(self):
        if self.api is not None:
            return
        try:
            info = InMemoryAccountInfo()
            self.api = B2Api(info)
            self.api.authorize_account("production", self.key_id, self.application_key)
            self.bucket = self.api.get_bucket_by_name(self.bucket_name)
            logger.info("Backblaze B2 client authorized successfully.")
        except Exception as e:
            logger.error(f"Failed to authorize Backblaze B2: {e}")
            raise e

    async def upload_file(self, local_path: str, filename: str) -> str:
        import asyncio
        await asyncio.to_thread(self._init_b2)
        
        logger.info(f"Uploading '{filename}' to B2 bucket '{self.bucket_name}'...")
        try:
            # Run in executor to avoid blocking the event loop
            file_info = await asyncio.to_thread(
                self.bucket.upload_local_file,
                local_file_path=local_path,
                file_name=filename
            )
            file_id = file_info.id_
            download_url = self.api.get_download_url_for_fileid(file_id)
            logger.info(f"B2 upload complete. URL: {download_url}")
            return download_url
        except Exception as e:
            logger.error(f"Error uploading file to B2: {e}")
            raise e

    async def download_file(self, file_identifier: str, local_destination: str) -> str:
        import asyncio
        await asyncio.to_thread(self._init_b2)
        
        logger.info(f"Downloading '{file_identifier}' from B2 to '{local_destination}'...")
        try:
            # Assumes file_identifier is the file name in the B2 bucket
            await asyncio.to_thread(
                self.bucket.download_file_by_name,
                file_name=file_identifier,
                download_dest_path=local_destination
            )
            return local_destination
        except Exception as e:
            logger.error(f"Error downloading file from B2: {e}")
            raise e

    async def delete_file(self, file_identifier: str) -> bool:
        import asyncio
        await asyncio.to_thread(self._init_b2)
        
        logger.info(f"Deleting '{file_identifier}' from B2...")
        try:
            file_version = await asyncio.to_thread(
                self.bucket.get_file_info_by_name,
                file_name=file_identifier
            )
            await asyncio.to_thread(
                self.api.delete_file_version,
                file_id=file_version.id_,
                file_name=file_identifier
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting file from B2: {e}")
            return False
