from abc import ABC, abstractmethod

class StorageProvider(ABC):
    """Abstract base class for all storage adapters."""
    
    @abstractmethod
    async def upload(self, file_path: str, destination_id: str) -> str:
        """Uploads a local file to the storage provider."""
        pass

    @abstractmethod
    async def download(self, source_id: str, destination_path: str) -> str:
        """Downloads a file from the storage provider to local disk."""
        pass
