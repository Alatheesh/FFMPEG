from abc import ABC, abstractmethod

class StorageProvider(ABC):
    
    @abstractmethod
    async def upload_file(self, local_path: str, filename: str) -> str:
        """
        Uploads a file from local storage to the provider.
        Returns a string identifier (e.g. file path, URL, or telegram file_id).
        """
        pass

    @abstractmethod
    async def download_file(self, file_identifier: str, local_destination: str) -> str:
        """
        Downloads a file from the provider to a local destination path.
        Returns the absolute local path.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_identifier: str) -> bool:
        """
        Deletes the file from the provider.
        """
        pass
