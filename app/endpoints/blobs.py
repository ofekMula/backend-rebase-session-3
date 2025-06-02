import mimetypes

from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from app.dependencies.storage_manager import StorageManager
from app.dependencies.validations import validate_blob_request
from app.models.responses import BlobCreatedResponse, BlobDeletedResponse
from app.settings import Settings

blobs_router = APIRouter()
app_settings = Settings()
storage_manager = StorageManager(
    storage_path=app_settings.storage_root,
    max_blobs_in_dir=app_settings.max_blobs_in_folder,
    chunk_size=app_settings.chunk_size,
)


@blobs_router.post("/blobs/{blob_id}")
async def create_blob(blob_id: str, request: Request, file: UploadFile):
    headers = dict(request.headers)
    stored_headers = {
        key: value for key, value in headers.items() if key == "content-type" or key.startswith("x-rebase")
    }
    validate_blob_request(
        blob_id,
        storage_manager.storage_metadata.used_bytes,
        headers,
        stored_headers,
        file,
    )
    try:
        storage_manager.save(
            blob_id=blob_id,
            blob=file.file,
            headers=stored_headers,
        )

        return BlobCreatedResponse(message=f"Blob '{blob_id}' created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving blob: {str(e)}")


@blobs_router.get("/blobs/{blob_id}")
async def get_blob(blob_id: str):
    try:
        blob_stream, metadata = storage_manager.stream_blob(blob_id)
        content_type = metadata.get("headers", {}).get("content-type")
        if not content_type:
            guess, _ = mimetypes.guess_type(blob_id)
            metadata["headers"]["Content-type"] = guess or "application/octet-stream"

        return StreamingResponse(
            content=blob_stream,
            media_type=metadata["headers"]["content-type"],
            headers=metadata["headers"],
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Blob '{blob_id}' not found")


@blobs_router.delete("/blobs/{blob_id}")
async def delete_blob(blob_id: str):
    try:
        storage_manager.delete(blob_id)
        return BlobDeletedResponse(message=f"Blob '{blob_id}' deleted successfully")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting blob: {str(e)}")
