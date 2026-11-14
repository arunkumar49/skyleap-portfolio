from typing import BinaryIO
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import BotoCoreError, ClientError
from botocore.client import BaseClient
from sky_leap.core.exceptions import StorageError
from sky_leap.domain.interfaces.infrastructure.storage.storage_interface import StorageInterface

class S3Storage(StorageInterface):
    def __init__(self, s3_client: BaseClient, bucket: str):
        self.s3 = s3_client
        self.bucket = bucket
        
        
    async def upload(self, fileObj: BinaryIO, key: str, content_type: str) -> None:
        try:
            self.s3.upload_fileobj(
                fileObj, self.bucket, key,
                ExtraArgs={"ContentType": content_type},
            )
            
        except (ClientError, BotoCoreError, S3UploadFailedError) as exc:
            raise StorageError(key) from exc