@echo off
echo ========================================================
echo Starting GigBid Multi-Agent Copilot
echo ========================================================

echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "GigBid Backend API" cmd /k ".venv\Scripts\python -m uvicorn apps.api.main:app --port 8000 --reload"

echo [2/2] Starting React/Vite Frontend on http://localhost:3000 ...
start "GigBid Frontend Web" cmd /k "cd apps\web && npm.cmd run dev"

echo.
echo GigBid is starting! 
echo Open your browser to: http://localhost:3000
echo ========================================================

