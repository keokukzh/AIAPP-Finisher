@echo off
REM ==============================================================================
REM KI-Projektmanagement-System - Production Start Script
REM Modern UI + FastAPI Backend + Claude-Flow Integration
REM ==============================================================================

cls
echo.
echo ========================================
echo  KI-Projektmanagement-System
echo  Production Start Script
echo ========================================
echo.

REM Check if running in Docker mode
if "%1"=="docker" goto docker_mode

:local_mode
echo [MODE] Local Development
echo.

REM Step 1: Kill existing processes
echo [1/5] Cleaning up existing processes...
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force" 2>nul
timeout /t 2 /nobreak >nul
echo       Done!

REM Step 2: Check Python
echo [2/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo       ERROR: Python not found!
    echo       Install from: https://www.python.org/
    pause
    exit /b 1
)
echo       Python found!

REM Step 3: Check Node.js (for Claude-Flow)
echo [3/5] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo       WARNING: Node.js not found!
    echo       Claude-Flow features will be limited.
    echo       Install from: https://nodejs.org/
) else (
    echo       Node.js found!
)

REM Step 4: Start Backend
echo [4/5] Starting FastAPI Backend (Port 8000)...
start "Backend API" cmd /k "python app.py"
timeout /t 5 /nobreak >nul

REM Step 5: Start Modern UI
echo [5/5] Starting Modern Streamlit UI (Port 8501)...
start "Modern UI" cmd /k "streamlit run streamlit_app_modern.py --server.port 8501"
timeout /t 5 /nobreak >nul

goto check_health

:docker_mode
echo [MODE] Docker Production
echo.

REM Check if Docker is running
echo [1/3] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo       ERROR: Docker not found!
    echo       Install from: https://www.docker.com/
    pause
    exit /b 1
)
echo       Docker found!

echo [2/3] Building Docker images...
docker-compose build
if errorlevel 1 (
    echo       ERROR: Docker build failed!
    pause
    exit /b 1
)

echo [3/3] Starting Docker containers...
docker-compose up -d
if errorlevel 1 (
    echo       ERROR: Docker start failed!
    pause
    exit /b 1
)

:check_health
echo.
echo ========================================
echo  Services Started!
echo ========================================
echo.

if "%1"=="docker" (
    echo  Mode: Docker Production
    echo  Backend API:  http://localhost:8000
    echo  Modern UI:    http://localhost:8501
    echo  API Docs:     http://localhost:8000/docs
    echo  MongoDB:      localhost:27017
    echo  Redis:        localhost:6379
) else (
    echo  Mode: Local Development
    echo  Backend API:  http://localhost:8000
    echo  Modern UI:    http://localhost:8501
    echo  API Docs:     http://localhost:8000/docs
)

echo.
echo ========================================
echo  Health Checks (wait 10 seconds...)
echo ========================================
timeout /t 10 /nobreak >nul

echo.
echo Checking Backend API...
curl -s http://localhost:8000/status >nul 2>&1
if errorlevel 1 (
    echo   WARNING: Backend not responding yet
) else (
    echo   OK: Backend is healthy!
)

echo Checking Modern UI...
curl -s http://localhost:8501 >nul 2>&1
if errorlevel 1 (
    echo   WARNING: UI not responding yet
) else (
    echo   OK: UI is accessible!
)

echo.
echo ========================================
echo  Opening browser...
echo ========================================
start http://localhost:8501

echo.
echo ========================================
echo  System Ready!
echo ========================================
echo.
echo Press any key to view logs or close...
pause >nul

