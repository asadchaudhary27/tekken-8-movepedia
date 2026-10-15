@echo off
title TEKKEN 8 MOVEPEDIA — Database Initializer
color 0B

cd /d "%~dp0"

echo =====================================================================
echo           TEKKEN 8 MOVEPEDIA - DATABASE INITIALIZER
echo =====================================================================
echo.

set "PYTHONPATH=%~dp0"
set "PYTHONIOENCODING=utf-8"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv!
    pause
    exit /b 1
)

echo [*] Initializing SQLite database and seeding 43 fighters & moves...
echo.

".venv\Scripts\python.exe" -c "
from backend.app.database.session import SessionLocal
from backend.app.database.init_db import init_db
db = SessionLocal()
try:
    init_db(db)
    print('Database initialized and seeded successfully!')
finally:
    db.close()
"

echo.
echo =====================================================================
echo Database initialization completed.
echo =====================================================================
pause
