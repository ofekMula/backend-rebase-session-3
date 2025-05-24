from pydantic import BaseModel, Field


class BlobCreatedResponse(BaseModel):
    message: str = Field(..., description="Confirmation that the blob was created")


class BlobDeletedResponse(BaseModel):
    message: str = Field(..., description="Confirmation that the blob was deleted")


class BlobRetrievedResponse(BaseModel):
    message: str = Field(..., description="Confirmation that the blob was retrieved")
    content: str = Field(..., description="Base64-encoded binary blob content")
    headers: dict[str, str] = Field(default_factory=dict, description="User-provided headers stored with the blob")
