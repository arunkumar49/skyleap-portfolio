from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageInterface(ABC):
    
    @abstractmethod
    async def upload(self, fileObj: BinaryIO, key: str, content_type: str) -> None:
        """Implement this method for uploading provided files to persistent storage."""