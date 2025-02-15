#!/bin/bash
# backend/start.sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🚀 Setting up the backend..."

# Check for Python installation
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 not found! Please install it."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Load environment variables from .env (if exists)
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Start FastAPI server with auto-reload enabled
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
