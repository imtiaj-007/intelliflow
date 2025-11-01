import uuid

from pydantic import BaseModel, Field, field_validator


class EmbeddingRequest(BaseModel):
    """Text and metadata for generating embeddings."""

    document_id: uuid.UUID
    chunks: list[str] = Field(..., min_length=1, description="Text chunks to embed")

    @field_validator("chunks")
    def validate_chunks(cls, v: list[str]):
        if not v:
            raise ValueError("At least one text chunk is required")

        # Filter out empty chunks but warn about them
        non_empty_chunks = [chunk for chunk in v if chunk and chunk.strip()]
        if len(non_empty_chunks) != len(v):
            print("⚠️ Warning: Some empty chunks were filtered out")

        return non_empty_chunks


class EmbeddingVector(BaseModel):
    """Represents a single text chunk and its vector embedding."""

    chunk_index: int = Field(..., ge=0, description="Position in original chunks list")
    text: str = Field(..., min_length=1, description="Original chunk text")

    @field_validator("vector")
    def validate_vector(cls, v):
        if not v:
            raise ValueError("Vector cannot be empty")
        if any(not isinstance(x, (int, float)) for x in v):
            raise ValueError("Vector must contain only numbers")
        return v


class EmbeddingResult(BaseModel):
    """Full embedding result for a document."""

    document_id: uuid.UUID
    embeddings: list[EmbeddingVector] = Field(..., min_length=1, description="Generated embeddings")

    @field_validator("embeddings")
    def validate_embeddings(cls, v: list[EmbeddingVector]):
        if not v:
            raise ValueError("At least one embedding is required")

        # Validate indices are unique
        indices = [embedding.chunk_index for embedding in v]
        if len(indices) != len(set(indices)):
            raise ValueError("Embedding chunk indices must be unique")

        return v
