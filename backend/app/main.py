"""
Tekken 8 Movepedia & Training Assistant - Main Application Entrypoint.
FastAPI application with OpenAPI docs, CORS, domain exceptions, and static asset serving.
"""

from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.core.errors import DomainException, domain_exception_handler
from backend.app.database.session import SessionLocal
from backend.app.database.init_db import init_db
from backend.app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database schema and seed data on startup."""
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Comprehensive Tekken 8 Frame Data, Move Reference, "
        "Notation Visualization, and Training Assistant REST API."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(DomainException, domain_exception_handler)

# Include API Routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Static Frontend Mounts
if os.path.exists("frontend"):
    app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

    @app.get("/", include_in_schema=False)
    def serve_index():
        return FileResponse("frontend/index.html")
