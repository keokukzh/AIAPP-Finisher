@echo off
REM ==============================================================================
REM KI-Projektmanagement-System - Stop Script
REM Clean shutdown of all services
REM ==============================================================================

cls
echo.
echo ========================================
echo  KI-Projektmanagement-System
echo  Stop Script
echo ========================================
echo.

if "%1"=="docker" goto docker_stop

:local_stop
echo [MODE] Stopping Local Services
echo.

echo [1/3] Stopping Python processes...
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force"
if errorlevel 1 (
    echo       No Python processes found
) else (
    echo       Done!
)

echo [2/3] Freeing ports 8000 and 8501...
powershell -Command "$ports = Get-NetTCPConnection -LocalPort 8000,8501 -State Listen -ErrorAction SilentlyContinue; if ($ports) { $ports | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }"
echo       Done!

echo [3/3] Cleaning up...
timeout /t 2 /nobreak >nul
echo       Done!

goto end

:docker_stop
echo [MODE] Stopping Docker Services
echo.

echo [1/2] Stopping Docker containers...
docker-compose down
if errorlevel 1 (
    echo       WARNING: Docker stop failed
) else (
    echo       Done!
)

echo [2/2] Cleaning up Docker resources (optional)...
echo       Skipping (use 'docker-compose down -v' to remove volumes)

:end
echo.
echo ========================================
echo  All Services Stopped!
echo ========================================
echo.
echo Ports 8000 and 8501 are now free.
echo.
pause

