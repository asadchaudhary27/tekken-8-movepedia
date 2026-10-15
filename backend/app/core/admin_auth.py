from typing import Optional
from fastapi import Header, HTTPException, status
from backend.app.core.config import settings


def verify_admin_token(
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
    x_admin_user: Optional[str] = Header("Administrator", alias="X-Admin-User"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """
    Enforces administrator credentials for data management operations.
    Accepts X-Admin-Key header or Authorization: Bearer <key>.
    Returns the acting administrator identity.
    """
    token = x_admin_key
    if not token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() in ["bearer", "token", "apikey"]:
            token = parts[1]
        else:
            token = authorization

    if not token or token != settings.ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authorization key is required or invalid. Access denied.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return x_admin_user or "Administrator"
