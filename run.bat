@echo off
title TEKKEN 8 MOVEPEDIA — Training Assistant & Frame Data
color 0C

cd /d "%~dp0"

echo =====================================================================
echo                TEKKEN 8 MOVEPEDIA - FYP SERVER
echo       Frame Data, Move Reference, Notation & Training Assistant
echo =====================================================================
echo.

set "PYTHONPATH=%~dp0"
set "PYTHONIOENCODING=utf-8"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv!
    echo Please make sure the project dependencies are installed.
    pause
    exit /b 1
)

echo [*] Starting FastAPI server on http://127.0.0.1:8000 ...
echo [*] Interactive OpenAPI Docs: http://127.0.0.1:8000/docs
echo [*] Opening browser in 2 seconds...
echo.

start "" "http://127.0.0.1:8000"

".venv\Scripts\python.exe" scripts\run_server.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server terminated with an error.
    pause
)
