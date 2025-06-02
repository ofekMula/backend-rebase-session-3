import re
from typing import Any

from fastapi import HTTPException, UploadFile

from app.settings import Settings

settings = Settings()
VALID_BLOB_ID_REGEX = re.compile(r"^[a-zA-Z0-9._-]+$")


def validate_blob_request(
    blob_id: str,
    used_bytes: int,
    headers: dict,
    stored_headers: dict[str, Any],
    file: UploadFile,
):
    if "content-length" not in headers:
        raise HTTPException(status_code=400, detail="Content-Length header is required")

    if len(stored_headers) > settings.max_header_count:
        raise HTTPException(
            status_code=400,
            detail=f"Too many headers, maximum allowed is {settings.max_header_count}",
        )

    if any(
        len(key) > settings.max_header_length or len(value) > settings.max_header_length
        for key, value in stored_headers.items()
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Header key or value length exceeds maximum allowed {settings.max_header_length} characters",
        )

    if sum(file.size + len(key) + len(value) for key, value in stored_headers.items()) > settings.max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Total size of headers and file exceeds maximum allowed {settings.max_length} bytes",
        )
    if used_bytes + file.size > settings.max_disk_quota:
        raise HTTPException(
            status_code=400,
            detail=f"Disk quota exceeded, maximum allowed is {settings.max_disk_quota} bytes",
        )
    if len(blob_id) > settings.max_id_length:
        raise HTTPException(
            status_code=400,
            detail=f"Blob ID length exceeds maximum allowed {settings.max_id_length} characters",
        )
    if not VALID_BLOB_ID_REGEX.match(blob_id):
        raise HTTPException(
            status_code=400,
            detail="Blob ID can only contain alphanumeric characters, dots, underscores, and hyphens",
        )
