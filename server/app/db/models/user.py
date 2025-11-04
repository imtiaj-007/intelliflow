import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import ConfigDict
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.schema.enums import UserRole

if TYPE_CHECKING:
    from app.db.models.file import File
    from app.db.models.workflow import Workflow


class User(Base):
    """
    User schema representing system users.
    """

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": "kdcdnj19eew5A5dcnKOW",
                "username": "john_doe",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "hashed_password",
                "role": "user",
                "is_active": True,
                "is_blocked": False,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T15:30:00Z",
            }
        },
    )

    __tablename__ = "users"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the user.",
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        index=True,
        comment="Unique username, optional.",
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        index=True,
        comment="Full name of the user, optional.",
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
        comment="User's email address (unique).",
    )
    password: Mapped[str] = mapped_column(
        String(255),
        default=None,
        nullable=False,
        comment="Hashed password for authentication.",
    )
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER,
        nullable=False,
        comment="User role (e.g., Admin, Anonymous, User).",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Indicates if the user account is active.",
    )
    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Indicates if the user is blocked from logging in.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the user was created.",
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the user was last updated.",
    )

    # Relationships
    user_sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    workflows: Mapped[list["Workflow"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    files: Mapped[list["File"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


class UserSession(Base):
    """
    User session schema representing user sessions in the system.
    """

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": "kdcdnj19eewe5A5dcnKOW",
                "user_id": "kdcdnj19eewe5A5dcnKOW",
                "session_token": "session_token_12345",
                "fingerprint_hash": "fingerprint_hash_abc123",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "browser": "Chrome",
                "os": "Windows",
                "device_type": "desktop",
                "screen_resolution": "1920x1080",
                "timezone": "UTC+05:30",
                "language": "en-IN",
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:30:00Z",
                "last_activity": "2025-01-01T12:30:00Z",
                "is_active": True,
            }
        },
    )

    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the user session.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.users.id", ondelete="CASCADE"),
        default=None,
        nullable=False,
        index=True,
        comment="ID of the user who owns the session.",
    )
    session_token: Mapped[str] = mapped_column(
        String(),
        nullable=False,
        index=True,
        comment="Cookie-based session token for authentication.",
    )
    fingerprint_hash: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="Hash of browser/device fingerprint for session tracking.",
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
        comment="IP address of the user's device.",
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="User agent string from the browser.",
    )
    browser: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Browser name and version.",
    )
    os: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Operating system of the user's device.",
    )
    device_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Type of device (desktop, mobile, tablet).",
    )
    device_vendor: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Manufacturer/vendor of the device (e.g., Apple, Samsung, Dell).",
    )
    device_model: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Specific model name of the device (e.g., iPhone 16, Galaxy S24, XPS 13).",
    )
    screen_resolution: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Screen resolution of the device.",
    )
    timezone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Timezone of the user's location.",
    )
    language: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        comment="Language preference of the user.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the session was created.",
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="Timestamp when the session was last updated.",
    )
    last_activity: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=True,
        comment="Timestamp of the last activity in this session.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Indicates if the session is currently active.",
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(back_populates="user_sessions")
