from enum import Enum


class UserRole(str, Enum):
    """Enum representing different user types."""

    ADMIN = "admin"
    ANONYMOUS = "anonymous"
    USER = "user"


class FileType(str, Enum):
    """Enum representing different file types."""

    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"


class MIMEType(str, Enum):
    """Enum representing common MIME types for file handling."""

    PDF = "application/pdf"
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    MP4 = "video/mp4"
    MP3 = "audio/mp3"
    TXT = "text/plain"
    CSV = "text/csv"
    JSON = "application/json"
    ZIP = "application/zip"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


class FileStatus(str, Enum):
    """Enum representing current file status."""

    UPLOADED = "uploaded"
    EMBEDDED = "embedded"
    FAILED = "failed"
