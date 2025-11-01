import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from pydantic import ConfigDict
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.schema.enums import FileStatus

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.workflow import Workflow


class File(Base):
    """
    File schema representing uploaded files in the system.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "kdcdnj19eewe5A5dcnKOW",
                "user_id": "kdcdnj19eewe5A5dcnKOW",
                "workflow_id": "kdcdnj19eewe5A5dcnKOW",
                "filename": "document.pdf",
                "s3_key": "uploads/kdcdnj19eewe5A5dcnKOW/document.pdf",
                "status": "embedded",
                "file_metadata": {
                    "content_type": "application/pdf",
                    "size": 2097152,
                    "pages": 10,
                    "author": "IntelliFlow",
                },
                "processed": True,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:30:00Z",
            }
        }
    )

    __tablename__ = "files"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the file.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.users.id"),
        index=True,
        nullable=False,
        comment="ID of the user who uploaded the file.",
    )
    workflow_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.workflows.id"),
        index=True,
        nullable=True,
        comment="Workflow ID of the file (Optional).",
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Original name of the uploaded file.",
    )
    s3_key: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        comment="S3 storage key/path for the file.",
    )
    status: Mapped[FileStatus] = mapped_column(
        default=FileStatus.UPLOADED,
        nullable=False,
        comment="Current file status ex: uploaded, embedded, failed",
    )
    file_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        default=None,
        nullable=True,
        comment="Metadata of the file ex: { 'content_type': 'application/pdf' }",
    )
    processed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Indicates if the file has been processed.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the file was uploaded.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the file was last updated.",
    )

    # Relationship
    user: Mapped["User"] = relationship(back_populates="files")
    embeddings: Mapped[list["FileEmbedding"]] = relationship(
        back_populates="file", cascade="all, delete-orphan", passive_deletes=True
    )
    workflow: Mapped["Workflow"] = relationship(
        back_populates="files", cascade="all, delete-orphan", passive_deletes=True
    )


class FileEmbedding(Base):
    """
    File embedding schema representing vector embeddings of document chunks.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "kdcdnj19eewe5A5dcnKOW",
                "file_id": "kdcdnj19eewe5A5dcnKOW",
                "chroma_id": "kdcdnj19eewe5A5dcnKOW_7",
                "chunk_index": 0,
                "chunk_text": "text chunk of a document",
                "embedding_metadata": {"text_length": 512, "model": "gemini-embedding-001"},
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:30:00Z",
            }
        }
    )

    __tablename__ = "file_embeddings"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the file embedding.",
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.files.id"),
        index=True,
        nullable=False,
        comment="ID of the associated file.",
    )
    chroma_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Unique identifier for the document chunk in ChromaDB vector store.",
    )
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Index of the chunk within the document.",
    )
    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="The actual text content of this chunk.",
    )
    embedding_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        default=None,
        nullable=True,
        comment="JSON containing additional embedding metadata.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the embedding was created.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the embedding was last updated.",
    )

    # Relationships
    file: Mapped["File"] = relationship(back_populates="embeddings")
