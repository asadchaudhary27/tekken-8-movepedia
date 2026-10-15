from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database.session import get_db
from backend.app.core.config import settings

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, summary="System Health Check")
def health_check(db: Session = Depends(get_db)):
    """
    Returns system status, database connectivity, and runtime settings.
    """
    db_status = "unhealthy"
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "database": db_status
    }
