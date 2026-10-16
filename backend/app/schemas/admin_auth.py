from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator


class AdminLoginRequest(BaseModel):
    username_or_email: Optional[str] = Field(None, description="Admin username or registered email address")
    identifier: Optional[str] = Field(None, description="Alias for username_or_email")
    password: str = Field(..., min_length=1, description="Account password")
    totp_code: Optional[str] = Field(None, description="6-digit TOTP Authenticator code if 2FA is active")

    @model_validator(mode='after')
    def validate_identifier(self):
        val = self.username_or_email or self.identifier
        if not val:
            raise ValueError("username_or_email or identifier is required")
        self.username_or_email = val
        return self



class AdminUserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str
    totp_enabled: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminLoginResponse(BaseModel):
    access_token: Optional[str] = None
    token_type: str = "bearer"
    requires_2fa: bool = False
    user: Optional[AdminUserRead] = None
    message: str = "Authentication successful"


class AdminUserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field("Admin", pattern="^(SuperAdmin|Admin|Editor)$")


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=8)


class TOTPSetupResponse(BaseModel):
    secret: str
    provisioning_uri: str
    qr_code_base64: str
    manual_entry_key: str


class TOTPVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=8)


class TOTPDisableRequest(BaseModel):
    password: str


class FighterBioUpdateRequest(BaseModel):
    height: Optional[str] = None
    weight: Optional[str] = None
    origin: Optional[str] = None
    fighting_style: Optional[str] = None
    bio_summary: Optional[str] = None
    avatar_url: Optional[str] = None
