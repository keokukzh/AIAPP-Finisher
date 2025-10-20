@echo off
cd /d C:\Users\keoku\Desktop\APP-Finisher
echo Starting FastAPI Backend Server...
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause

