# Quick Start Script for Banking AI Agent (PowerShell)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Banking AI Agent - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

# Activate venv
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env and add your OpenAI API Key" -ForegroundColor Red
    Write-Host "Run: notepad .env" -ForegroundColor Yellow
    Write-Host ""
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q
Write-Host "Dependencies installed!" -ForegroundColor Green

# Check if initial setup is done
if (-not (Test-Path "backend\data\banking_docs.txt")) {
    Write-Host ""
    Write-Host "Initializing sample data..." -ForegroundColor Yellow
    python backend\data_init.py
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Terminal 1 - Start Backend:" -ForegroundColor White
Write-Host "   python -m uvicorn backend.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Terminal 2 - Start Frontend:" -ForegroundColor White
Write-Host "   streamlit run frontend/app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
