# SafeRide Backend Startup Script

Write-Host "Starting SafeRide Backend..." -ForegroundColor Green

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Start the server
Write-Host "Starting Uvicorn server on http://localhost:8000" -ForegroundColor Cyan
python -m uvicorn app.main:create_app --reload --host 0.0.0.0 --port 8000
