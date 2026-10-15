@echo off
title TEKKEN 8 MOVEPEDIA — Test Suite Runner
color 0A

cd /d "%~dp0"

echo =====================================================================
echo           TEKKEN 8 MOVEPEDIA - AUTOMATED PYTEST SUITE
echo =====================================================================
echo.

set "PYTHONPATH=%~dp0"
set "PYTHONIOENCODING=utf-8"

if not exist ".venv\Scripts\pytest.exe" (
    echo [ERROR] pytest not found in .venv!
    pause
    exit /b 1
)

echo [*] Executing backend test suite with verbose output...
echo.

".venv\Scripts\pytest.exe" -v backend\tests

echo.
echo =====================================================================
echo Tests execution finished.
echo =====================================================================
pause
