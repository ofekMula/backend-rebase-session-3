import hashlib
import json
import logging
import os
from collections.abc import Generator
from pathlib import Path
from typing import BinaryIO

from app.models.storage import StorageMeta

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, storage_path: str, max_blobs_in_dir: int, chunk_size: int):
        logger.info("Initializing StorageManager on location: %s", storage_path)

        self.storage_path = Path(storage_path)
        os.makedirs(self.storage_path, exist_ok=True)
        self.storage_metadata_path = self.storage_path.joinpath("storage_meta.json")

        self.storage_metadata: StorageMeta = self._load_storage_metadata()

        self.max_blobs_in_dir = max_blobs_in_dir
        self.chunk_size = chunk_size

    def _load_storage_metadata(self) -> StorageMeta:
        if self.storage_metadata_path.exists():
            with open(self.storage_metadata_path) as f:
                return StorageMeta.model_validate(json.load(f))
        return StorageMeta()

    def _save_index(self):
        with open(self.storage_metadata_path, "w") as f:
            json.dump(self.storage_metadata.model_dump(), f)

    def _get_blob_dir_name(self, blob_id: str) -> str:
        return hashlib.md5(blob_id.encode()).hexdigest()[:2]

    def _get_blob_path(self, blob_id: str) -> Path:
        return self.storage_path.joinpath(self._get_blob_dir_name(blob_id), f"{blob_id}.blob")

    def _get_metadata_path(self, blob_id: str) -> Path:
        return self.storage_path.joinpath(self._get_blob_dir_name(blob_id), f"{blob_id}.meta.json")

    def _create_new_blob_dir(self, new_dir_name: str) -> str:
        """Create a new blob directory based on the current number of directories."""
        logger.info("Creating new blob directory: %s", new_dir_name)
        os.makedirs(self.storage_path / new_dir_name, exist_ok=True)
        return new_dir_name

    def _load_blob_directories(self) -> list[str]:
        """Load existing blob directories from the storage path."""
        return [d.name for d in self.storage_path.iterdir() if d.is_dir()]

    def save(self, blob_id: str, blob: BinaryIO, headers: dict[str, str] | None = None):
        logger.info("Saving blob: %s", blob_id)

        dir_name = self._get_blob_dir_name(blob_id)
        dir_path = self.storage_path / dir_name
        if not dir_path.exists():
            self._create_new_blob_dir(dir_name)

        blob_path = self._get_blob_path(blob_id)
        blob_md_path = self._get_metadata_path(blob_id)
        blob_md_content = {
            "headers": headers or {},
        }
        if blob_path.exists():
            self.storage_metadata.used_bytes -= blob_path.stat().st_size

        with open(blob_path, "wb") as f:
            while chunk := blob.read(self.chunk_size):
                self.storage_metadata.used_bytes += len(chunk)
                f.write(chunk)

        with open(blob_md_path, "w") as f:
            f.write(json.dumps(blob_md_content))

        self._save_index()

    def stream_blob(self, blob_id: str) -> tuple[bytes, dict[str, str] | None]:
        logger.info("Loading blob: %s", blob_id)

        if not self._blob_exists(blob_id):
            raise FileNotFoundError(f"Blob '{blob_id}' not found")

        blob_path = self._get_blob_path(blob_id)
        metadata_path = self._get_metadata_path(blob_id)

        def stream_blob() -> Generator[bytes, None, None]:
            with open(blob_path, "rb") as f:
                while chunk := f.read(self.chunk_size):
                    yield chunk

        metadata = {}
        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)

        return stream_blob(), metadata

    def delete(self, blob_id: str):
        logger.info("Deleting blob: %s", blob_id)

        blob_path = self._get_blob_path(blob_id)
        if blob_path.exists():
            blob_size = blob_path.stat().st_size
            headers_path = self._get_metadata_path(blob_id)

            blob_path.unlink()
            if headers_path.exists():
                headers_path.unlink()

            self.storage_metadata.used_bytes -= blob_size
            self._save_index()

    def _blob_exists(self, blob_id: str) -> bool:
        return self._get_blob_path(blob_id).exists()
