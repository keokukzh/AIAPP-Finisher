@echo off
cd /d C:\Users\keoku\Desktop\APP-Finisher
echo Starting Streamlit UI...
echo Frontend URL: http://localhost:8501
echo.
timeout /t 5 /nobreak
streamlit run streamlit_app_modern.py --server.port 8501 --server.address 0.0.0.0
pause

