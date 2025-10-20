#!/bin/bash

# Start script for KI-Projektmanagement-System

echo "🚀 Starting KI-Projektmanagement-System..."

# Start FastAPI Backend in background
echo "📡 Starting FastAPI Backend..."
uvicorn app:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! curl -f http://localhost:8000/status > /dev/null 2>&1; then
    echo "❌ FastAPI Backend failed to start"
    exit 1
fi

echo "✅ FastAPI Backend started successfully"

# Start Streamlit UI
echo "🎨 Starting Streamlit UI..."
if [ -f "streamlit_app_modern.py" ]; then
    streamlit run streamlit_app_modern.py --server.port 8501 --server.address 0.0.0.0
else
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
fi

# Cleanup function
cleanup() {
    echo "🛑 Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

# Trap signals for graceful shutdown
trap cleanup SIGTERM SIGINT

# Wait for background process
wait $BACKEND_PID
