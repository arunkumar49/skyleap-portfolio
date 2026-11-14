from functools import lru_cache

import boto3
from sky_leap.core.config import get_settings
from sky_leap.infrastructure.storage.s3_storage import S3Storage
from sky_leap.services.document_service import DocumentService


config = get_settings()


@lru_cache
def get_document_service() -> DocumentService:
    storage = S3Storage(boto3.client("s3"), config.aws_s3_bucket)
    return DocumentService(storage=storage)