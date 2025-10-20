@echo off
echo ========================================
echo KI-Projektmanagement-System Log Viewer
echo ========================================
echo.
echo Aktuelle Python-Prozesse:
tasklist | findstr python
echo.
echo ========================================
echo Log-Ausgabe anzeigen:
echo ========================================
echo.
echo 1. FastAPI Backend (Port 8000):
echo    - URL: http://localhost:8000/status
echo    - API Docs: http://localhost:8000/docs
echo.
echo 2. Streamlit UI (Port 8501):
echo    - URL: http://localhost:8501
echo.
echo 3. Log-Ausgabe in separaten Fenstern:
echo    - Backend Logs: Siehe Terminal wo "python app.py" läuft
echo    - UI Logs: Siehe Terminal wo "streamlit run streamlit_app.py" läuft
echo.
echo ========================================
echo Teste Verbindungen:
echo ========================================
echo.
echo Teste Backend...
curl -s http://localhost:8000/status
echo.
echo.
echo Teste Streamlit UI...
curl -s -I http://localhost:8501
echo.
echo ========================================
echo System bereit! Oeffnen Sie:
echo - http://localhost:8501 (Streamlit UI)
echo - http://localhost:8000/docs (API Docs)
echo ========================================
pause
