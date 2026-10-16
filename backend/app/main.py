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
    try:
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()
    except Exception as e:
        import logging
        logging.getLogger("uvicorn.error").warning(f"Database lifespan startup warning: {e}")
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


# Vercel Serverless Path Normalization Middleware
class VercelPathMiddleware:
    """
    Normalizes request paths when deployed on Vercel or Serverless environments.
    Resolves x-matched-path headers and strips internal /api/index.py rewrite prefixes.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            matched_path = headers.get(b"x-matched-path")
            if matched_path:
                try:
                    decoded = matched_path.decode("latin1")
                    if not decoded.startswith("/api/index"):
                        scope["path"] = decoded
                except Exception:
                    pass

            path = scope.get("path", "/")
            if path in ("/api/index.py", "/api/index", "/api", "/api/"):
                scope["path"] = "/"
            elif path.startswith("/api/index.py/"):
                scope["path"] = path[len("/api/index.py"):]
            elif path.startswith("/api/index/"):
                scope["path"] = path[len("/api/index"):]

        await self.app(scope, receive, send)


app.add_middleware(VercelPathMiddleware)

# Exception Handlers
app.add_exception_handler(DomainException, domain_exception_handler)

# Include API Routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Static Frontend Mounts
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_dir = os.path.join(ROOT_DIR, "frontend")
if not os.path.exists(frontend_dir) and os.path.exists("frontend"):
    frontend_dir = os.path.abspath("frontend")

if os.path.exists(frontend_dir):
    assets_dir = os.path.join(frontend_dir, "assets")
    index_html = os.path.join(frontend_dir, "index.html")
    presentation_html = os.path.join(frontend_dir, "presentation.html")

    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    if os.path.exists(index_html):
        @app.get("/", include_in_schema=False)
        @app.get("/api/index.py", include_in_schema=False)
        @app.get("/api/index", include_in_schema=False)
        @app.get("/api", include_in_schema=False)
        @app.get("/api/", include_in_schema=False)
        def serve_index():
            return FileResponse(index_html)

    if os.path.exists(presentation_html):
        @app.get("/presentation", include_in_schema=False)
        def serve_presentation():
            return FileResponse(presentation_html)

