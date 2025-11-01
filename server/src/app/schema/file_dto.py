import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schema.enums import FileStatus, MIMEType


class FileUploadRequest(BaseModel):
    file_name: str
    file_size: int
    file_ext: str


class FileMetadata(BaseModel):
    extension: str
    mime_type: MIMEType
    size: int | None = None
    pages: int | None = None
    author: str | None = None


class FileBase(BaseModel):
    id: uuid.UUID = Field(..., description="Unique identifier for the file.")
    user_id: uuid.UUID = Field(..., description="ID of the user who uploaded the file.")
    workflow_id: Optional[uuid.UUID] = Field(
        None, description="Workflow ID of the file (Optional)."
    )
    filename: str = Field(..., description="Original name of the uploaded file.")
    s3_key: str = Field(..., description="S3 key/path where the file is stored.")
    status: FileStatus = Field(..., description="Current status of the file.")
    file_metadata: Dict[str, Any] = Field(..., description="Metadata about the file content.")
    processed: bool = Field(..., description="Indicates if the file has been processed.")
    created_at: datetime = Field(..., description="Timestamp when the file was created.")
    updated_at: datetime = Field(..., description="Timestamp when the file was last updated.")


class FileCreate(BaseModel):
    user_id: uuid.UUID = Field(..., description="ID of the user who uploaded the file.")
    workflow_id: Optional[uuid.UUID] = Field(
        None, description="Workflow ID of the file (Optional)."
    )
    filename: str = Field(..., description="Original name of the uploaded file.")
    s3_key: str = Field(..., description="S3 key/path where the file is stored.")
    file_metadata: Dict[str, Any] = Field(..., description="Metadata about the file content.")


class FileUpdate(BaseModel):
    workflow_id: Optional[uuid.UUID] = Field(
        None, description="Workflow ID of the file (Optional)."
    )
    status: Optional[FileStatus] = Field(None, description="Current status of the file.")
    file_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Metadata about the file content."
    )
    processed: Optional[bool] = Field(None, description="Indicates if the file has been processed.")


class FileRead(FileBase):
    pass


class FileEmbeddingBase(BaseModel):
    id: uuid.UUID = Field(..., description="Unique identifier for the file embedding.")
    file_id: uuid.UUID = Field(..., description="ID of the associated file.")
    chroma_id: str = Field(
        ..., description="Unique identifier for the document chunk in ChromaDB vector store."
    )
    chunk_index: int = Field(..., description="Index of the chunk within the document.")
    chunk_text: str = Field(..., description="The actual text content of this chunk.")
    embedding_metadata: Optional[Dict[str, Any]] = Field(
        None, description="JSON containing additional embedding metadata."
    )
    created_at: datetime = Field(..., description="Timestamp when the embedding was created.")
    updated_at: datetime = Field(..., description="Timestamp when the embedding was last updated.")


class FileEmbeddingCreate(BaseModel):
    file_id: uuid.UUID = Field(..., description="ID of the associated file.")
    chroma_id: str = Field(
        ..., description="Unique identifier for the document chunk in ChromaDB vector store."
    )
    chunk_index: int = Field(..., description="Index of the chunk within the document.")
    chunk_text: str = Field(..., description="The actual text content of this chunk.")
    embedding_metadata: Optional[Dict[str, Any]] = Field(
        None, description="JSON containing additional embedding metadata."
    )


class FileEmbeddingUpdate(BaseModel):
    chunk_text: Optional[str] = Field(None, description="The actual text content of this chunk.")
    embedding_metadata: Optional[Dict[str, Any]] = Field(
        None, description="JSON containing additional embedding metadata."
    )


class FileEmbeddingRead(FileEmbeddingBase):
    pass


class PresignedUrlResponse(BaseModel):
    url: str
    file_key: str
    expires_in: int
    id: uuid.UUID | None = None
    mime_type: MIMEType | None = None
