@echo off
REM Nano Stories Setup Script for Windows
REM This script helps set up the Nano Stories project for development

echo 🚀 Nano Stories Setup
echo =====================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.13+ first.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Node.js is not installed. Frontend linting will be skipped.
    set HAS_NODE=false
) else (
    set HAS_NODE=true
    echo ✅ Node.js detected
)

REM Create virtual environment
echo.
echo 📦 Setting up Python virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo.
echo 📦 Installing backend dependencies...
pip install -r backend\requirements.txt

REM Initialize database
echo.
echo 🗄️  Initializing database...
cd backend
python -c "from src.database import init_database; init_database()"
cd ..

REM Setup frontend (optional)
if "%HAS_NODE%"=="true" (
    echo.
    echo 📦 Setting up frontend...
    cd frontend
    npm install
    cd ..
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your GOOGLE_API_KEY
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Google Gemini API key
echo 2. Run: venv\Scripts\activate.bat
echo 3. Start backend: cd backend && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
echo 4. Start frontend: cd frontend && python -m http.server 3000
echo 5. Open http://localhost:3000 in your browser
echo.
echo 📚 For detailed instructions, see README.md

pause
