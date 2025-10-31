from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schema.enums import UserRole


class UserBase(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the user.")
    username: Optional[str] = Field(None, description="Unique username, optional.", max_length=50)
    name: Optional[str] = Field(None, description="Full name of the user, optional.", max_length=50)
    email: EmailStr = Field(
        ..., description="User's email address (unique but optional).", max_length=100
    )
    role: UserRole = Field(..., description="User role (e.g., Admin, Anonymous, User).")
    is_active: bool = Field(..., description="Indicates if the user account is active.")
    is_blocked: bool = Field(..., description="Indicates if the user is blocked from logging in.")
    created_at: datetime = Field(..., description="Timestamp when the user was created.")
    updated_at: datetime = Field(..., description="Timestamp when the user was last updated.")

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    role: Optional[UserRole] = Field(UserRole.USER)
    is_active: Optional[bool] = Field(True)
    is_blocked: Optional[bool] = Field(False)

    class Config:
        from_attributes = True


class UserRead(UserBase):
    pass


class UserLogin(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)


class LoginResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str
    session_id: str


class UserSessionBase(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the user session.")
    user_id: UUID = Field(..., description="ID of the user who owns the session.")
    session_token: str | None = Field(
        None, description="Cookie-based session token for authentication."
    )
    fingerprint_hash: str | None = Field(
        None, description="Hash of browser/device fingerprint for session tracking.", max_length=255
    )
    ip_address: str | None = Field(
        None, description="IP address of the user's device.", max_length=45
    )
    user_agent: str | None = Field(
        None, description="User agent string from the browser.", max_length=500
    )
    browser: str | None = Field(None, description="Browser name and version.", max_length=100)
    os: str | None = Field(
        None, description="Operating system of the user's device.", max_length=100
    )
    device_type: Optional[str] = Field(
        None, description="Type of device (desktop, mobile, tablet).", max_length=50
    )
    device_vendor: Optional[str] = Field(
        None, description="Manufacturer/vendor of the device.", max_length=100
    )
    device_model: Optional[str] = Field(
        None, description="Specific model name of the device.", max_length=100
    )
    screen_resolution: Optional[str] = Field(
        None, description="Screen resolution of the device.", max_length=20
    )
    timezone: str | None = Field(
        None, description="Timezone of the user's location.", max_length=50
    )
    language: str | None = Field(
        None, description="Language preference of the user.", max_length=10
    )
    created_at: datetime = Field(..., description="Timestamp when the session was created.")
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the session was last updated."
    )
    last_activity: Optional[datetime] = Field(
        None, description="Timestamp of the last activity in this session."
    )
    is_active: bool = Field(..., description="Indicates if the session is currently active.")

    class Config:
        from_attributes = True


class UserSessionCreate(BaseModel):
    user_id: UUID
    session_token: str
    fingerprint_hash: str = Field(None, max_length=255)
    ip_address: str = Field(None, max_length=45)
    user_agent: str = Field(None, max_length=500)
    browser: str = Field(None, max_length=100)
    os: str = Field(None, max_length=100)
    device_type: Optional[str] = Field(None, max_length=50)
    device_vendor: Optional[str] = Field(None, max_length=100)
    device_model: Optional[str] = Field(None, max_length=100)
    screen_resolution: Optional[str] = Field(None, max_length=20)
    timezone: str = Field(None, max_length=50)
    language: str = Field(None, max_length=10)

    class Config:
        from_attributes = True


class UserSessionRead(UserSessionBase):
    pass
