@echo off
REM Certificate Platform - Setup Script for Windows

echo =========================================
echo Certificate Management System Setup
echo =========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.9+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js not found. Please install Node.js 16+
    exit /b 1
)

echo OK: Prerequisites found
echo.

REM Backend Setup
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy ..\configs\.env.example .env
    echo WARNING: Please update .env with your database credentials
)

cd ..

REM Frontend Setup
echo.
echo Setting up Frontend...
cd frontend

echo Installing Node dependencies...
call npm install -q

cd ..

REM Create startup scripts
echo.
echo Creating startup scripts...

(
    echo @echo off
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo pause
) > start_backend.bat

(
    echo @echo off
    echo cd frontend
    echo npm run dev
    echo pause
) > start_frontend.bat

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next Steps:
echo 1. Update backend\.env with your configuration
echo 2. Start Backend: start_backend.bat
echo 3. Start Frontend (new terminal): start_frontend.bat
echo.
echo Access the application:
echo   Frontend: http://localhost:5173
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Default Credentials:
echo   Username: admin
echo   Password: admin123
echo.
pause
