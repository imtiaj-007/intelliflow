import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import get_current_user, get_file_service
from app.schema.file_dto import FileUploadRequest, PresignedUrlResponse
from app.service.file import FileService

router = APIRouter()


@router.post("/upload", response_model=PresignedUrlResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: FileUploadRequest,
    current_user: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for uploading a file to S3.

    This endpoint creates a file record in the database and returns a presigned URL
    that can be used to upload the file directly to S3 storage.

    Args:
        file (FileUploadRequest): File upload request containing:
            - file_name: Name of the file to be uploaded
            - file_size: Size of the file in bytes
            - file_ext: File extension
        current_user (uuid.UUID): ID of the authenticated user (from dependency)
        file_service (FileService): Injected file service dependency

    Returns:
        PresignedUrlResponse: Response containing:
            - id: UUID of the created file record
            - url: Presigned URL for S3 upload
            - file_key: S3 key where the file will be stored
            - mime_type: Detected MIME type of the file
            - expires_in: URL expiration time in seconds

    Raises:
        HTTPException:
            - 400: If filename or file size validation fails
            - 413: If file size exceeds maximum allowed limit
            - 500: If internal server error occurs during file creation
    """
    try:
        return await file_service.create_file(user_id=current_user, file=file)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate upload URL",
        )


@router.post("/{file_id}/process", status_code=status.HTTP_202_ACCEPTED)
async def process_file(
    file_id: uuid.UUID,
    current_user: uuid.UUID = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> dict:
    """
    Process a file to extract text and generate embeddings.

    This endpoint triggers the processing of an uploaded file by:
    1. Downloading the file from S3
    2. Extracting text content
    3. Splitting into chunks
    4. Generating embeddings
    5. Storing embeddings in vector database
    6. Saving embedding metadata in database

    Args:
        file_id (uuid.UUID): ID of the file to process
        current_user (uuid.UUID): ID of the authenticated user (from dependency)
        file_service (FileService): Injected file service dependency

    Returns:
        dict: Response containing processing status message

    Raises:
        HTTPException:
            - 404: If file not found
            - 403: If user doesn't own the file
            - 500: If processing fails
    """
    try:
        success = await file_service.process_file(file_id)

        if success:
            return {"status": "success", "message": f"File {file_id} processed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File processing failed"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}",
        )
