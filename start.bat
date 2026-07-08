@echo off
REM RAG ChatBot Quick Start Script for Windows

echo.
echo ============================================================
echo         RAG ChatBot - Quick Start
echo ============================================================
echo.
echo This script will start all services. Make sure:
echo - Qdrant is running (docker run -p 6333:6333 qdrant/qdrant)
echo - You have 3 terminals available
echo.
pause

echo.
echo [1/3] Starting FastAPI Backend...
echo.
cd /d D:\go\rag-pipeline
set PYTHONPATH=.
start "RAG Backend" cmd /k "python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 3 /nobreak

echo.
echo [2/3] Starting Next.js Frontend...
echo.
cd /d D:\go\rag-pipeline\chatbot
start "RAG Frontend" cmd /k "npm run dev"

echo.
echo ============================================================
echo         ✅ Services Starting!
echo ============================================================
echo.
echo Backend API:   http://localhost:8000
echo API Docs:      http://localhost:8000/docs
echo Frontend:      http://localhost:3000
echo Qdrant:        http://localhost:6333/dashboard
echo.
echo Press any key to exit this window...
echo (Services will continue running in separate windows)
echo.
pause
