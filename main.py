"""
Tekken 8 Movepedia & Fighter Intelligence Platform - Root Entrypoint.
Exposes the FastAPI 'app' instance for cloud deployment buildpacks,
Cloud Run, Uvicorn, Render, Railway, and local execution.
"""

import sys
import os

# Ensure workspace root is in Python module search path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Expose primary FastAPI application
from backend.app.main import app  # noqa: E402

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=False)
