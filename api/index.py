"""
Vercel Serverless Function Entrypoint for Tekken 8 Movepedia.
Exposes the FastAPI application instance `app`.
"""

import sys
import os

# Ensure the root project directory is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app.main import app  # noqa: E402

__all__ = ["app"]
