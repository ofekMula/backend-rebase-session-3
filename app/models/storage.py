from pydantic import BaseModel


class StorageMeta(BaseModel):
    used_bytes: int = 0
