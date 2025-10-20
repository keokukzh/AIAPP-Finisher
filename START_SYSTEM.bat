@echo off
echo ========================================
echo   KI-PROJEKTMANAGEMENT-SYSTEM
echo   Starting Refactored System...
echo ========================================
echo.
cd /d C:\Users\keoku\Desktop\APP-Finisher

echo [1/2] Starting FastAPI Backend...
start "KI System - Backend" cmd /k "python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo [3/3] Starting Streamlit Frontend...
start "KI System - Frontend" cmd /k "streamlit run streamlit_app_modern.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ========================================
echo   SYSTEM STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:8501
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:8501
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /F /FI "WINDOWTITLE eq KI System*" 2>nul
echo Done!

