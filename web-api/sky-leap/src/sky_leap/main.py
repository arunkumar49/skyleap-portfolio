from typing import Any
from sky_leap.api.v1.endpoints import documents
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sky_leap.core.exceptions import StorageError
from sky_leap.api.v1.endpoints import chat

app = FastAPI()

app.include_router(documents.router)
app.include_router(chat.router)

@app.exception_handler(StorageError)
async def storage_error_handler(request: Request, exc: StorageError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": "Could not store the file"})


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}