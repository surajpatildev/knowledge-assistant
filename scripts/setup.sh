#!/bin/bash

# Data Lens Setup Script
# ======================

set -e

echo "🚀 Data Lens Setup Script"
echo "========================="

# Check for required tools
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check pnpm
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is required but not installed."
    echo "Installing pnpm..."
    npm install -g pnpm
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ is required but not installed."
    echo "Please install Python from https://python.org/"
    exit 1
fi

# Check Poetry
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is required but not installed."
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "⚠️  You may need to restart your terminal or run:"
    echo "source ~/.bashrc  # or ~/.zshrc"
    echo "Please restart and run this script again."
    exit 1
fi

echo "✅ All prerequisites found!"

# Check external services
echo "🔍 Checking external services..."

# Check PostgreSQL
if timeout 5 bash -c '</dev/tcp/localhost/5432' 2>/dev/null; then
    echo "✅ PostgreSQL is accessible on localhost:5432"
else
    echo "⚠️  PostgreSQL not accessible on localhost:5432"
    echo "Please ensure your external PostgreSQL is running"
    echo "Update DATABASE_URL in .env if using different host/port"
fi

# Check Redis  
if timeout 5 bash -c '</dev/tcp/localhost/6379' 2>/dev/null; then
    echo "✅ Redis is accessible on localhost:6379"
else
    echo "⚠️  Redis not accessible on localhost:6379"
    echo "Please ensure your external Redis is running"
    echo "Update REDIS_URL in .env if using different host/port"
fi

# Install dependencies
echo "📦 Installing JavaScript dependencies..."
pnpm install

echo "🐍 Installing Python dependencies with Poetry..."
cd apps/api
poetry config virtualenvs.in-project false
poetry install
cd ../..

# Copy environment files
echo "📝 Setting up environment files..."
if [ ! -f apps/web/.env.local ]; then
    cp apps/web/.env.local.example apps/web/.env.local
    echo "✅ Created apps/web/.env.local"
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env"
    echo "⚠️  Please update DATABASE_URL and REDIS_URL in .env to match your external services"
fi

echo ""
echo "🎉 Setup complete!"
echo "==================="
echo ""
echo "🔧 External Services Required:"
echo "  PostgreSQL: Update DATABASE_URL in .env"
echo "  Redis: Update REDIS_URL in .env"
echo ""
echo "🗄️ Database Setup:"
echo "  Run: psql -U postgres -d data_lens -f docker/init-db/01-init.sql"
echo "  (Adjust connection parameters as needed)"
echo ""
echo "🌐 Available URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "🚀 To start development:"
echo "  make dev"
echo ""
echo "🐍 Poetry Commands:"
echo "  make poetry-shell     - Enter Poetry virtual environment"
echo "  make poetry-show      - Show dependency tree"
echo "  make poetry-add       - Add new package"
echo ""
echo "📚 Other commands:"
echo "  make help           - Show all available commands"
echo "  make status         - Check service status"
echo "  make check-services - Test external service connectivity"
echo "  make check-deps     - Verify all tools are installed"
echo ""