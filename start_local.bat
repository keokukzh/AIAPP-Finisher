@echo off
echo Starting KI-Projektmanagement-System...

REM Start FastAPI Backend
echo Starting FastAPI Backend on port 8000...
start "FastAPI Backend" python app.py

REM Wait for backend
timeout /t 5 /nobreak

REM Start Streamlit UI  
echo Starting Streamlit UI on port 8501...
start "Streamlit UI" streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

echo.
echo System started successfully!
echo FastAPI: http://localhost:8000
echo Streamlit: http://localhost:8501
echo.
echo Press Ctrl+C in each window to stop
pause
