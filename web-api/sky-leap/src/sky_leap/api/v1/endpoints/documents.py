from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import Field
from sky_leap.api.dependencies import get_document_service
from sky_leap.core.exceptions import UnsupportedFileTypeError
from sky_leap.services.document_service import DocumentService



router = APIRouter(
    prefix="/document",
    tags=["documents"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/uploadfile"
)
async def upload_document(
    file: Annotated[UploadFile, Field(description="")],
    service: Annotated[DocumentService, Depends(get_document_service)]
) -> dict[str, Any]:
    """
    Upload a document to storage for the RAG knowledge base.

    The file is stored under `data/rag/<filename>`. Only the base filename is
    kept, so any directory part is stripped. Uploading a file with the same
    name overwrites the existing one.

    **Allowed file types:** `.pdf`, `.txt`, `.md`, `.docx`

    **Returns:** the storage key of the uploaded file, e.g. `{"key": "data/rag/resume.pdf"}`.

    **Errors:**
    - `400`: the file type is not allowed.
    - `502`: the file could not be written to storage.
    """
    try:
        key = await service.upload_document(file.file, file.filename, file.content_type)
        # return {"filename": file.filename, "filesize": file.size}
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"key": key}
