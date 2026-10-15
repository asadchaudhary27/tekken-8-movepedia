"""
CLI script to initialize the SQLite database schema and seed all 43 characters and verified moves.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.database.session import SessionLocal
from backend.app.database.init_db import init_db


def main():
    print("Initializing Tekken 8 Movepedia database...")
    db = SessionLocal()
    try:
        init_db(db)
        print("Success: Database schema created and verified records seeded.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
