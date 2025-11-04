import uuid
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.db.models.file import File, FileEmbedding
from app.schema.file_dto import FileCreate, FileEmbeddingCreate
from app.utils.logger import log


class FileRepository:
    """
    Repository class for handling database operations related to files.

    This class provides CRUD operations for the File model using SQLAlchemy
    with async database sessions.

    Attributes:
        session (AsyncSession): The async database session used for all operations
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the FileRepository with a database session.

        Args:
            db_session (AsyncSession): The async database session to use for operations
        """
        self.session = db_session

    async def create(self, file: FileCreate) -> Optional[File]:
        """
        Create a new file record in the database.

        Args:
            file (FileCreate): The FileCreate object to create

        Returns:
            Optional[File]: The created File object if successful, None if error occurs

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            file_data = File(**file.model_dump())
            self.session.add(file_data)
            await self.session.commit()
            await self.session.refresh(file_data)
            return file_data
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error creating file record: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error creating file record: {e}")
            raise

    async def get_file_by_id(self, file_id: uuid.UUID) -> Optional[File]:
        """
        Retrieve a file record by its unique identifier.

        Args:
            file_id (uuid.UUID): The UUID of the file to retrieve

        Returns:
            Optional[File]: The File object if found, None if no file exists with the given ID

        Raises:
            SQLAlchemyError: If there's a database error during the operation
            Exception: If any other unexpected error occurs during the operation
        """
        try:
            q = select(File).where(File.id == file_id)
            res = await self.session.execute(q)
            return res.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error getting file by id: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error getting file by id: {e}")
            raise

    async def get_file_by_workflow_id(self, workflow_id: uuid.UUID) -> Optional[File]:
        """
        Retrieve a file record by its associated workflow identifier.

        Args:
            workflow_id (uuid.UUID): The UUID of the workflow to search for files

        Returns:
            Optional[File]: The File object if found, None if no file exists with the given workflow ID

        Raises:
            SQLAlchemyError: If there's a database error during the operation
            Exception: If any other unexpected error occurs during the operation
        """
        try:
            q = select(File).where(File.workflow_id == workflow_id)
            res = await self.session.execute(q)
            return res.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error getting file by workflow_id: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error getting file by workflow_id: {e}")
            raise

    async def get_user_files(self, user_id: uuid.UUID) -> Sequence[File]:
        """
        Retrieve all files belonging to a specific user.

        Args:
            user_id (uuid.UUID): The UUID of the user whose files to retrieve

        Returns:
            Sequence[File]: Sequence of File objects belonging to the user, empty sequence if none found

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            q = select(File).where(File.user_id == user_id)
            res = await self.session.execute(q)
            return res.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error getting user files: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error getting user files: {e}")
            raise
        

    async def save_embeddings(
        self,
        file_id: uuid.UUID,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        stored_ids: List[str],
    ) -> bool:
        """
        Save file embeddings to the database.

        Args:
            file_id (uuid.UUID): The UUID of the file to associate embeddings with
            embeddings (List[EmbeddingVector]): List of embedding vector DTOs to save

        Returns:
            bool: True if embeddings were successfully saved, False otherwise

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            embeddings_data = []
            for text, metadata, chroma_id in zip(texts, metadatas, stored_ids):
                embedding_data = FileEmbeddingCreate(
                    file_id=file_id,
                    chroma_id=chroma_id,
                    chunk_index=metadata["chunk_index"],
                    chunk_text=text,
                    embedding_metadata={
                        "text_length": len(text),
                        "model": settings.LLM_EMBEDDING_MODEL,
                        "page": metadata["page"],
                        "source": metadata["source"],
                    },
                )
                embeddings_data.append(FileEmbedding(**embedding_data.model_dump()))

            self.session.add_all(embeddings_data)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error saving embeddings for document {file_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error saving embeddings for document {file_id}: {e}")
            raise

    async def get_file_embeddings(self, file_id: uuid.UUID) -> Sequence[FileEmbedding]:
        """
        Retrieve all embeddings for a specific file.

        Args:
            file_id (uuid.UUID): The UUID of the file whose embeddings to retrieve

        Returns:
            Sequence[FileEmbedding]: Sequence of FileEmbedding objects for the document,
                empty sequence if none found

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            q = select(FileEmbedding).where(FileEmbedding.file_id == file_id)
            res = await self.session.execute(q)
            return res.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error retrieving embeddings for document {file_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error retrieving embeddings for document {file_id}: {e}")
            raise

    async def get_document_content(self, file_id: uuid.UUID) -> Optional[str]:
        """
        Retrieve the full text content of a document by concatenating all its chunks.

        Args:
            file_id (uuid.UUID): The UUID of the document to retrieve content for

        Returns:
            Optional[str]: The concatenated text content of all document chunks,
                or None if an error occurs or no content is found

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            q = select(FileEmbedding).where(FileEmbedding.file_id == file_id)
            result = await self.session.execute(q)
            doc_embeddings = result.scalars().all()
            return " ".join([row.chunk_text for row in doc_embeddings])
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error retrieving embeddings for document {file_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error retrieving embeddings for document {file_id}: {e}")
            raise

    async def get_chunks_by_indices(
        self, user_id: uuid.UUID, indices: List[int]
    ) -> List[Tuple[uuid.UUID, int, str]]:
        """
        Retrieve document chunks by their indices for a specific document.

        Args:
            user_id (uuid.UUID): The UUID of the user
            indices (List[int]): List of chunk indices to retrieve

        Returns:
            List[Tuple[uuid.UUID, int, str]]: List of tuples containing (file_id, chunk_index, chunk_text)
                for the specified indices, empty list if none found

        Raises:
            SQLAlchemyError: If there's a database error during the operation
        """
        try:
            if not indices:
                return []

            q = (
                select(
                    FileEmbedding.file_id,
                    FileEmbedding.chunk_index,
                    FileEmbedding.chunk_text,
                )
                .join(File, FileEmbedding.file_id == File.id)
                .where(
                    File.user_id == user_id,
                    FileEmbedding.chunk_index.in_(indices),
                )
            )
            result = await self.session.execute(q)
            return [
                (file_id, chunk_index, chunk_text)
                for file_id, chunk_index, chunk_text in result.all()
            ]
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving chunks with indices {indices}: {e}")
            return []
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error retrieving chunks with indices {indices}: {e}")
            raise
