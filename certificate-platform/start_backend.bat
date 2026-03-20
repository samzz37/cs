@echo off
REM Start Backend Server

cd backend

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Error: Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

echo Starting Certificate Management System Backend...
echo.
echo Backend will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.

REM Start uvicorn server
python -m uvicorn asgi:app --reload --host 0.0.0.0 --port 8000

pause
