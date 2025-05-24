from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_length: int = 10 * 1024 * 1024
    max_disk_quota: int = 1 * 1024 * 1024 * 1024
    max_header_length: int = 100
    max_header_count: int = 20
    max_id_length: int = 200
    max_blobs_in_folder: int = 10_000
    chunk_size: int = 1024 * 1024  # 1 MB

    storage_root: str = "storage"
    index_file: str = "blob_index.json"
