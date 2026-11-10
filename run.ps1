# GigBid Quick Launch Script for PowerShell
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting GigBid Multi-Agent Copilot" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& .venv\Scripts\python -m uvicorn apps.api.main:app --port 8000 --reload"

Write-Host "[2/2] Starting React/Vite Frontend on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\web; npm.cmd run dev"

Start-Sleep -Seconds 2
Write-Host "`nGigBid is live!" -ForegroundColor Green
Write-Host "Open your browser to: " -NoNewline
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "Swagger API docs at:  " -NoNewline
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

