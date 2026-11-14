from pathlib import PurePosixPath
from typing import BinaryIO
from sky_leap.core.exceptions import UnsupportedFileTypeError
from sky_leap.domain.interfaces.infrastructure.storage.storage_interface import StorageInterface


class DocumentService:
    ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
    PREFIX = "data/rag"
    
    def __init__(self, storage: StorageInterface):
        self.storage = storage
        
    async def upload_document(
        self, fileobj: BinaryIO, filename: str | None, content_type: str | None
    ) -> str:
        name = PurePosixPath(filename or "").name
        if PurePosixPath(name).suffix.lower() not in self.ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError(name)

        key = f"{self.PREFIX}/{name}"
        await self.storage.upload(fileobj, key, content_type or "application/octet-stream")
        return key