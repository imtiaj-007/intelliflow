import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, status

from app.aws import AWSConfig
from app.schema.enums import MIMEType
from app.schema.file_dto import FileMetadata, PresignedUrlResponse
from app.utils.logger import log


class S3Manager:
    """
    Manager class for handling S3 operations with comprehensive error handling and caching.

    This class provides methods for file uploads, generating presigned URLs, and other
    S3 operations with built-in validation, error handling, and performance optimizations.

    Attributes:
        config (AWSConfig): Configuration instance for AWS settings
        _client (Optional[boto3.client]): Cached S3 client instance
        SAFE_FILENAME_REGEX (Pattern): Regular expression for validating safe filenames
        ALLOWED_EXTENSIONS (set): Set of allowed file extensions
        MAX_FILE_SIZE (int): Maximum allowed file size in bytes (2MB)
        MIME_TYPES (Dict[str, str]): Mapping of file extensions to MIME types
    """

    def __init__(self):
        """
        Initialize the S3 manager with configuration and default settings.

        Sets up the S3 client configuration, filename validation regex, allowed extensions,
        maximum file size limit, and MIME type mappings for supported file types.
        """
        self.config = AWSConfig()
        self._client = None
        self.UPLOAD_FOLDER = "intelliflow/uploads"
        self.SAFE_FILENAME_REGEX = re.compile(r"^[\w\-. ]+$")
        self.ALLOWED_EXTENSIONS = set([".pdf", ".doc", ".docx", ".txt"])
        self.MAX_FILE_SIZE = 2097152  # 2MB
        self.MIME_TYPES = {
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".txt": "text/plain",
        }

    @property
    def client(self):
        """
        Cached S3 client property with singleton pattern.

        Returns:
            boto3.client: Configured S3 client instance

        Note:
            The client is cached to ensure only one instance is created and reused
            throughout the application lifecycle, improving performance and connection
            management.
        """
        try:
            if self._client is None:
                self._client = boto3.client(
                    "s3",
                    region_name=self.config.region,
                    aws_access_key_id=self.config.aws_access_key,
                    aws_secret_access_key=self.config.aws_secret_key,
                    config=Config(signature_version="s3v4"),
                )
            return self._client
        except Exception as e:
            log.error(f"Error creating S3 client: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize S3 client",
            )

    def _validate_file_params(self, filename: str, file_size: Optional[int] = None) -> FileMetadata:
        """
        Validate file parameters against configured file type constraints.

        This method performs comprehensive validation including filename safety,
        file extension compatibility, MIME type mapping, and size constraints.

        Args:
            filename (str): Name of the file to validate
            file_size (Optional[int]): Size of the file in bytes (optional for validation)

        Returns:
            FileMetadata: Validated file information containing:
                - extension: File extension (e.g., '.pdf')
                - mime_type: Corresponding MIME type as MIMEType enum
                - size: Validated file size (None if not provided)

        Raises:
            ValueError: If filename is empty, filename format is invalid,
                file extension is not allowed, or no MIME type mapping exists
            HTTPException: If file size exceeds the configured maximum limit (413 status)
        """
        try:
            if not filename:
                raise ValueError("Filename must not be empty")

            if not self.SAFE_FILENAME_REGEX.match(filename):
                raise ValueError("Invalid filename format")

            file_path = Path(filename)
            ext = file_path.suffix.lower()

            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file extension for {ext}. Allowed: {self.ALLOWED_EXTENSIONS}"
                )

            mime_type = self.MIME_TYPES.get(ext)
            if mime_type is None:
                raise ValueError(f"Unsupported mime type for {ext}")

            if file_size and file_size > self.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                    detail=f"File size should be within {self.MAX_FILE_SIZE / 1048576}MB",
                )

            return FileMetadata(extension=ext, mime_type=MIMEType(mime_type), size=file_size)
        except HTTPException:
            raise
        except Exception as e:
            log.error(f"Error validating file parameters: {str(e)}")
            raise ValueError(f"File validation failed: {str(e)}")

    def _build_file_key(self, filename: str) -> str:
        """
        Construct a unique and sanitized S3 file key with timestamp.

        This method generates a unique filename by appending a timestamp to the
        original filename stem and ensures the folder path is properly formatted
        for S3 compatibility.

        Args:
            filename (str): Original filename

        Returns:
            str: Unique S3 file key in the format 'folder/base_timestamp.extension'
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = Path(filename)
            base = file_path.stem
            ext = file_path.suffix
            unique_filename = f"{base}_{timestamp}{ext}"

            # Sanitize folder path and convert to S3-compatible format
            return f"{self.UPLOAD_FOLDER}/{unique_filename}"
        except Exception as e:
            log.error(f"Error building file key for {filename}: {str(e)}")
            raise ValueError(f"Failed to generate file key: {str(e)}")

    def download_file(self, file_key: str) -> bytes:
        """
        Download a file from S3 by its key and return as bytes.

        Args:
            file_key (str): The S3 key of the file to download

        Returns:
            bytes: The file content as bytes

        Raises:
            HTTPException:
                - 404 if file is not found
                - 500 for AWS credential errors, S3 operation failures, or unexpected errors
        """
        try:
            response = self.client.get_object(Bucket=self.config.bucket_name, Key=file_key)
            body: bytes = response["Body"].read()
            return body
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                log.error(f"File not found in S3: {file_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {file_key}"
                )
            elif error_code in ["AccessDenied", "Forbidden"]:
                log.error(f"AWS access denied for file: {file_key}, error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Access denied to S3 resource",
                )
            else:
                log.error(f"AWS S3 error downloading file {file_key}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error downloading from S3",
                )
        except NoCredentialsError as e:
            log.error(f"AWS credentials not found: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AWS credentials not found",
            )
        except Exception as e:
            log.error(f"Unexpected error downloading file {file_key}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during file download",
            )

    def generate_presigned_url(
        self,
        file_key: str,
        operation: str,  # 'get_object' or 'put_object'
        expiration: int = 3600,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a presigned URL with additional parameters and error handling.

        Args:
            file_key (str): The S3 key for the file operation
            operation (str): The S3 client method ('get_object' or 'put_object')
            expiration (int): URL expiration time in seconds (default: 3600)
            extra_params (Optional[Dict[str, Any]]): Additional parameters for the S3 operation

        Returns:
            str: Presigned URL for the specified S3 operation

        Raises:
            HTTPException:
                - 500 for AWS credential errors, S3 operation failures, or unexpected errors
        """
        try:
            params = {"Bucket": self.config.bucket_name, "Key": file_key}
            if extra_params:
                params.update(extra_params)

            url = self.client.generate_presigned_url(
                ClientMethod=operation, Params=params, ExpiresIn=expiration
            )

            log.info(f"Generated presigned URL for operation: {operation}, key: {file_key}")
            return url

        except NoCredentialsError as e:
            log.error(f"AWS credentials not found: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AWS credentials not found",
            )
        except ClientError as e:
            log.error(f"AWS S3 error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generating presigned URL",
            )
        except Exception as e:
            log.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    def get_upload_url(
        self,
        filename: str,
        file_size: int,
        expiration: int = 3600,
    ) -> PresignedUrlResponse:
        """Generate a presigned URL for uploading files with type-specific validation"""
        file_info = self._validate_file_params(filename=filename, file_size=file_size)
        file_key = self._build_file_key(filename)

        extra_params = {
            "ContentType": file_info.mime_type.value,
            "ContentLength": file_info.size,
        }

        url = self.generate_presigned_url(
            file_key=file_key,
            operation="put_object",
            expiration=expiration,
            extra_params=extra_params,
        )

        return PresignedUrlResponse(
            url=url,
            file_key=file_key,
            expires_in=expiration,
            mime_type=file_info.mime_type,
        )

    def get_download_url(self, file_key: str, expiration: int = 3600) -> PresignedUrlResponse:
        """Generate a presigned URL for downloading files with type validation"""
        try:
            self.client.head_object(Bucket=self.config.bucket_name, Key=file_key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            raise

        url = self.generate_presigned_url(file_key, "get_object", expiration)

        return PresignedUrlResponse(url=url, file_key=file_key, expires_in=expiration)


class S3Instance:
    """
    Thread-safe singleton factory class for S3Manager instances.

    This class implements the double-checked locking pattern to ensure only one
    S3Manager instance is created and shared across the application, providing
    thread safety and efficient resource management for S3 operations.

    Attributes:
        _s3_manager_instance (Optional[S3Manager]): The singleton S3Manager instance
        _s3_manager_lock (threading.Lock): Lock for thread-safe singleton creation
    """

    _s3_manager_instance: Optional[S3Manager] = None
    _s3_manager_lock: threading.Lock = threading.Lock()

    @classmethod
    def get_s3_manager(cls) -> S3Manager:
        """
        Get or create the singleton S3Manager instance using thread-safe pattern.

        This method uses double-checked locking to ensure thread safety while
        maintaining performance by avoiding unnecessary lock acquisition.

        Returns:
            S3Manager: The singleton S3Manager instance for S3 operations

        Note:
            The singleton pattern ensures consistent S3 client configuration
            and connection reuse throughout the application lifecycle.
        """

        if cls._s3_manager_instance is None:
            with cls._s3_manager_lock:
                if cls._s3_manager_instance is None:
                    cls._s3_manager_instance = S3Manager()

        return cls._s3_manager_instance
