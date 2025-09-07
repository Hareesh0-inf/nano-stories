#!/bin/bash

# Nano Stories Setup Script
# This script helps set up the Nano Stories project for development

set -e

echo "🚀 Nano Stories Setup"
echo "===================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$(printf '%s\n' "$PYTHON_VERSION" "3.13" | sort -V | head -n1)" != "3.13" ]]; then
    echo "❌ Python $PYTHON_VERSION detected. Please upgrade to Python 3.13+"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. Frontend linting will be skipped."
    HAS_NODE=false
else
    HAS_NODE=true
    echo "✅ Node.js detected"
fi

# Create virtual environment
echo ""
echo "📦 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Initialize database
echo ""
echo "🗄️  Initializing database..."
cd backend
python3 -c "from src.database import init_database; init_database()"
cd ..

# Setup frontend (optional)
if [ "$HAS_NODE" = true ]; then
    echo ""
    echo "📦 Setting up frontend..."
    cd frontend
    npm install
    cd ..
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GOOGLE_API_KEY"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Google Gemini API key"
echo "2. Run: source venv/bin/activate"
echo "3. Start backend: cd backend && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload"
echo "4. Start frontend: cd frontend && python -m http.server 3000"
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For detailed instructions, see README.md"
