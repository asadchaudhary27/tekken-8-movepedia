import os
import shutil
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_url = settings.DATABASE_URL

# Vercel / AWS Lambda Serverless support (read-only root mitigation)
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    target_path = Path(tempfile.gettempdir()) / "tekken8_fyp.db"
    if not target_path.exists():
        source_candidates = [
            Path(ROOT_DIR) / "tekken8_fyp.db",
            Path(os.getcwd()) / "tekken8_fyp.db",
            Path("tekken8_fyp.db").resolve()
        ]
        for candidate in source_candidates:
            if candidate.exists():
                try:
                    shutil.copyfile(candidate, target_path)
                    break
                except Exception:
                    pass
    db_url = f"sqlite:///{target_path.as_posix()}"

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=settings.DEBUG and False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency for yielding database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
