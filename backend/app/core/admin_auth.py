from typing import Optional
from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.security import decode_access_token
from backend.app.database.session import get_db
from backend.app.models.admin_user import AdminUser


def verify_admin_token(
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
    x_admin_user: Optional[str] = Header(None, alias="X-Admin-User"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
) -> str:
    """
    Enforces administrator credentials for data management operations.
    Accepts:
    1. Cryptographically signed JWT Bearer Token (Authorization: Bearer <jwt>)
    2. Header X-Admin-Token or X-Admin-Key (JWT or Legacy Admin Secret Key fallback for tests)
    Returns the acting administrator username.
    """
    raw_token = x_admin_key
    if not raw_token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() in ["bearer", "token", "apikey"]:
            raw_token = parts[1]
        else:
            raw_token = authorization

    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authorization token is required. Access denied.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 1. Check if token is a cryptographically signed JWT
    payload = decode_access_token(raw_token)
    if payload:
        username = payload.get("username") or payload.get("sub")
        if username:
            # Check user in database
            user = db.query(AdminUser).filter_by(username=username).first()
            if user:
                return user.username
            return username

    # 2. Check legacy admin key fallback (for automated integration test suites)
    if raw_token == settings.ADMIN_SECRET_KEY:
        return x_admin_user or "Administrator"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin authorization token is invalid or expired. Access denied.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_admin_user(
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    Retrieves the authenticated AdminUser database entity.
    """
    raw_token = x_admin_key
    if not raw_token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() in ["bearer", "token", "apikey"]:
            raw_token = parts[1]
        else:
            raw_token = authorization

    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin credentials required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # JWT validation
    payload = decode_access_token(raw_token)
    if payload:
        username = payload.get("username") or payload.get("sub")
        user = db.query(AdminUser).filter_by(username=username).first()
        if user:
            return user

    # Fallback to initial master user if legacy secret matches
    if raw_token == settings.ADMIN_SECRET_KEY:
        user = db.query(AdminUser).filter_by(username=settings.INITIAL_ADMIN_USER).first()
        if user:
            return user
        # If user not created yet, return synthetic representation
        temp_user = AdminUser(
            id=1,
            username=settings.INITIAL_ADMIN_USER,
            email=settings.INITIAL_ADMIN_EMAIL,
            role="SuperAdmin",
            totp_enabled=False
        )
        return temp_user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired session token",
        headers={"WWW-Authenticate": "Bearer"}
    )
