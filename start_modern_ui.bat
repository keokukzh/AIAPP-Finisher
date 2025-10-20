@echo off
echo ========================================
echo KI-Projektmanagement-System
echo Moderne UI mit Claude-Flow
echo ========================================
echo.

echo [1/2] Starte FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /k "python app.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starte Moderne Streamlit UI (Port 8501)...
start "Modern UI" cmd /k "streamlit run streamlit_app_modern.py --server.port 8501"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Services wurden gestartet!
echo ========================================
echo.
echo FastAPI Backend:  http://localhost:8000
echo Moderne UI:       http://localhost:8501
echo API Docs:         http://localhost:8000/docs
echo.
echo Druecke eine Taste um fortzufahren...
pause >nul

