#!/bin/bash

# Development server startup script
# =================================

set -e

echo "🔥 Starting Data Lens Development Environment"
echo "============================================="

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Poetry
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is required but not installed."
    echo "Please install Poetry: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check Poetry environment
echo "🐍 Checking Poetry environment..."
cd apps/api
if poetry env info &> /dev/null; then
    echo "✅ Poetry environment is ready"
else
    echo "🔧 Setting up Poetry environment..."
    poetry install
fi
cd ../..

echo "✅ All services and dependencies are ready!"
echo ""
echo "🌐 URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down development servers..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start development servers
echo "🚀 Starting development servers..."
echo ""

# Start API server in background
echo "🐍 Starting API server..."
cd apps/api
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
cd ../..

# Wait a moment for API to start
sleep 2

# Start frontend server
echo "⚛️ Starting frontend server..."
pnpm dev &
WEB_PID=$!

# Wait for both processes
wait $API_PID $WEB_PID