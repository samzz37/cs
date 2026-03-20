@echo off
REM Start Frontend Development Server

cd frontend

echo Starting Certificate Management System Frontend...
echo.
echo Frontend will be available at: http://localhost:5173
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    echo.
)

REM Start development server
npm run dev

pause
