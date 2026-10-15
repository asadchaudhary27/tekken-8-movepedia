from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.source import DataSource
from backend.app.schemas.source import DataSourceResponse

router = APIRouter()


@router.get("", response_model=List[DataSourceResponse], summary="List audited data sources and approval status")
def list_sources(db: Session = Depends(get_db)):
    sources = db.query(DataSource).all()
    return sources
