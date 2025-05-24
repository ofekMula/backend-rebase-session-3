from pydantic import BaseModel, Field


class StorageMeta(BaseModel):
    index: dict[str, str] = Field(default_factory=dict)  # blob_id -> dir_name
    used_bytes: int = 0
