@echo off
REM Quick Start Script for Banking AI Agent

echo.
echo ========================================
echo Banking AI Agent - Quick Start
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate venv
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your OpenAI API Key
    echo Using: notepad .env
    echo.
    pause
)

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt -q
echo Dependencies installed!

REM Check if initial setup is done
if not exist "backend\data\banking_docs.txt" (
    echo.
    echo Initializing sample data...
    python backend\data_init.py
)

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Terminal 1 - Start Backend:
echo    python -m uvicorn backend.main:app --reload
echo.
echo 2. Terminal 2 - Start Frontend:
echo    streamlit run frontend/app.py
echo.
echo Then open: http://localhost:8501
echo.
pause
