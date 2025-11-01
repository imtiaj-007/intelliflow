import uuid

from fastapi import HTTPException, status

from app.ai.embedding_manager import EmbeddingManager
from app.aws.s3_manager import S3Manager
from app.repository.file import FileRepository
from app.schema.file_dto import FileCreate, FileMetadata, FileUploadRequest, PresignedUrlResponse
from app.utils.logger import log


class FileService:
    """
    Service class for handling file operations including S3 uploads and database management.

    This class coordinates between S3 operations for file storage and database operations
    for file metadata persistence, providing a unified interface for file creation and management.

    Attributes:
        s3_manager (S3Manager): Manager for S3 operations and presigned URL generation
        file_repo (FileRepository): Repository for database operations related to files
    """

    def __init__(
        self,
        s3_manager: S3Manager,
        embedding_manager: EmbeddingManager,
        file_repository: FileRepository,
    ):
        """
        Initialize the FileService with S3 manager and file repository dependencies.

        Args:
            s3_manager (S3Manager): Manager instance for S3 operations
            file_repository (FileRepository): Repository instance for database operations
        """
        self.s3_manager = s3_manager
        self.embedding_manager = embedding_manager
        self.file_repo = file_repository

    async def create_file(
        self, user_id: uuid.UUID, file: FileUploadRequest
    ) -> PresignedUrlResponse:
        """
        Create a new file record and generate a presigned upload URL.

        This method orchestrates the file creation process by:
        1. Generating a presigned URL for S3 upload
        2. Creating a file record in the database
        3. Returning the presigned URL response with file metadata

        Args:
            user_id (uuid.UUID): UUID of the user creating the file
            file (FileUploadRequest): File upload request containing:
                - file_name: Name of the file to be uploaded
                - file_size: Size of the file in bytes
                - file_ext: File extension

        Returns:
            PresignedUrlResponse: Response containing the presigned URL, file key,
                expiration time, MIME type, and created file ID

        Raises:
            HTTPException:
                - 500 if database creation fails
                - Propagates any exceptions from S3 operations or database operations
        """
        try:
            presigned_response = self.s3_manager.get_upload_url(
                filename=file.file_name, file_size=file.file_size
            )
            file = FileCreate(
                user_id=user_id,
                filename=file.file_name,
                s3_key=presigned_response.file_key,
                file_metadata=FileMetadata(
                    size=file.file_size,
                    extension=file.file_ext,
                    mime_type=presigned_response.mime_type,
                ).model_dump(),
            )
            result = await self.file_repo.create(file)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create file",
                )
            return PresignedUrlResponse(
                id=result.id,
                url=presigned_response.url,
                file_key=presigned_response.file_key,
                mime_type=presigned_response.mime_type,
                expires_in=presigned_response.expires_in,
            )
        except Exception as e:
            log.error(f"Error creating file: {e}")
            raise

    async def process_file(self, file_id: str | uuid.UUID) -> bool:
        """
        Process a file by its unique identifier.

        This method orchestrates the file processing process by:
        1. Retrieving the file record from the database
        2. Downloading the file content from S3
        3. Processing the file content using EmbeddingManager
        4. Storing the embeddings in ChromaDB
        5. Saving the embedding IDs in the database
        6. Returning the result of the processing
        """
        try:
            file_id = uuid.UUID(file_id) if isinstance(file_id, str) else file_id
            file = await self.file_repo.get_file_by_id(file_id)
            if not file:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

            # Download file content from S3
            file_content = self.s3_manager.download_file(file.s3_key)

            documents = self.embedding_manager.process_file_content(
                file_content=file_content,
                file_extension=f".{file.file_metadata.get('extension', 'pdf')}",
            )

            # Add documents to vector store and get stored IDs
            texts, metadatas, stored_ids = self.embedding_manager.add_documents_to_store(
                documents=documents, file_id=str(file_id)
            )

            # Save embedding IDs to database
            success = await self.file_repo.save_embeddings(
                file_id=file_id,
                texts=texts,
                metadatas=metadatas,
                stored_ids=stored_ids,
            )

            if not success:
                log.warning(f"Failed to save embedding IDs for file {file_id}")

            log.info(f"Successfully processed file {file_id} with {len(stored_ids)} embeddings")
            return True

        except Exception as e:
            log.error(f"Error processing file: {e}")
            raise
