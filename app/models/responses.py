from pydantic import BaseModel, Field


class BlobCreatedResponse(BaseModel):
    message: str = Field(..., description="Confirmation that the blob was created")


class BlobDeletedResponse(BaseModel):
    message: str = Field(..., description="Confirmation that the blob was deleted")
