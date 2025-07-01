# Data Lens - Development Makefile

.PHONY: help install dev build test lint format clean docker-api docker-web setup

# Default target
help: ## Show this help message
	@echo "Data Lens - Development Commands"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development setup
install: ## Install all dependencies (JavaScript + Python)
	@echo "📦 Installing dependencies..."
	pnpm install
	@echo "🐍 Installing Python dependencies with Poetry..."
	cd apps/api && poetry install

setup: install ## Development setup (requires external PostgreSQL and Redis)
	@echo "🚀 Setting up development environment..."
	@echo "⚠️  Make sure PostgreSQL and Redis are running externally"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Development commands
dev: ## Start development servers (requires external PostgreSQL and Redis)
	@echo "🔥 Starting development servers..."
	@echo "⚠️  Ensure PostgreSQL and Redis are running externally"
	@echo "🌐 URLs:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "🚀 Press Ctrl+C to stop all servers"
	@./scripts/dev.sh

dev-api: ## Start only the API server
	@echo "🐍 Starting API server with Poetry..."
	@echo "⚠️  Ensure PostgreSQL and Redis are running externally"
	@echo "🌐 API will be available at: http://localhost:5000"
	@echo "📚 API Docs: http://localhost:5000/docs"
	cd apps/api && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

dev-web: ## Start only the web server
	@echo "⚛️ Starting web server..."
	cd apps/web && pnpm dev

# Build commands
build: ## Build all packages
	@echo "🏗️ Building all packages..."
	pnpm build
	@echo "🐍 Building Python package..."
	cd apps/api && poetry build

build-api: ## Build API only
	@echo "🐍 Building API with Poetry..."
	cd apps/api && poetry build

build-web: ## Build web only
	@echo "⚛️ Building web app..."
	cd apps/web && pnpm build

# Testing
test: ## Run all tests
	@echo "🧪 Running tests..."
	pnpm test
	cd apps/api && poetry run pytest

test-api: ## Run API tests
	@echo "🐍 Running API tests with Poetry..."
	cd apps/api && poetry run pytest

test-web: ## Run web tests
	@echo "⚛️ Running web tests..."
	cd apps/web && pnpm test

# Code quality
lint: ## Run linters
	@echo "🔍 Running linters..."
	pnpm lint
	@echo "🐍 Running Python linters..."
	cd apps/api && poetry run flake8 app
	cd apps/api && poetry run mypy app

format: ## Format code
	@echo "✨ Formatting code..."
	pnpm format
	@echo "🐍 Formatting Python code..."
	cd apps/api && poetry run black app
	cd apps/api && poetry run isort app

type-check: ## Run TypeScript type checking
	@echo "🔍 Type checking..."
	pnpm type-check
	@echo "🐍 Type checking Python..."
	cd apps/api && poetry run mypy app

# Poetry-specific commands
poetry-install: ## Install Python dependencies with Poetry
	@echo "🐍 Installing Python dependencies..."
	cd apps/api && poetry install

poetry-add: ## Add a Python dependency (usage: make poetry-add PACKAGE=package-name)
	@echo "🐍 Adding Python package: $(PACKAGE)"
	cd apps/api && poetry add $(PACKAGE)

poetry-add-dev: ## Add a Python dev dependency (usage: make poetry-add-dev PACKAGE=package-name)
	@echo "🐍 Adding Python dev package: $(PACKAGE)"
	cd apps/api && poetry add --group dev $(PACKAGE)

poetry-show: ## Show Poetry dependency tree
	@echo "🐍 Poetry dependency tree:"
	cd apps/api && poetry show --tree

poetry-lock: ## Update Poetry lock file
	@echo "🐍 Updating Poetry lock file..."
	cd apps/api && poetry lock

poetry-shell: ## Enter Poetry shell
	@echo "🐍 Entering Poetry shell..."
	cd apps/api && poetry shell

# Docker commands (optional - for containerized development)
docker-api: ## Start API in Docker (connects to external PostgreSQL/Redis)
	@echo "🐳 Starting API container..."
	@echo "⚠️  Ensure PostgreSQL and Redis are running externally"
	docker-compose -f docker/docker-compose.dev.yml --profile api-only up -d

docker-web: ## Start Web in Docker
	@echo "🐳 Starting Web container..."
	docker-compose -f docker/docker-compose.dev.yml --profile web-only up -d

docker-down: ## Stop Docker containers
	@echo "🐳 Stopping Docker containers..."
	docker-compose -f docker/docker-compose.dev.yml down

docker-logs: ## Show docker logs
	@echo "📋 Showing docker logs..."
	docker-compose -f docker/docker-compose.dev.yml logs -f

docker-rebuild: ## Rebuild and restart containers
	@echo "🔄 Rebuilding containers..."
	docker-compose -f docker/docker-compose.dev.yml down
	docker-compose -f docker/docker-compose.dev.yml up -d --build

# Database commands (for external PostgreSQL)
db-init: ## Initialize database schema (run SQL manually)
	@echo "🗄️ Database initialization instructions:"
	@echo "Connect to your external PostgreSQL and run:"
	@echo "psql -U postgres -d data_lens -f docker/init-db/01-init.sql"

db-check: ## Check database connection
	@echo "🗄️ Checking database connection..."
	@echo "Ensure your external PostgreSQL is running on the configured URL"

db-migrate: ## Run database migrations with Alembic
	@echo "🗄️ Running database migrations..."
	cd apps/api && poetry run alembic upgrade head

db-migration: ## Create new database migration (usage: make db-migration MESSAGE="description")
	@echo "🗄️ Creating new migration: $(MESSAGE)"
	cd apps/api && poetry run alembic revision --autogenerate -m "$(MESSAGE)"

# Cleanup commands
clean: ## Clean build artifacts and dependencies
	@echo "🧹 Cleaning..."
	pnpm clean
	rm -rf node_modules
	find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".turbo" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

clean-docker: ## Clean Docker containers
	@echo "🧹 Cleaning Docker..."
	docker-compose -f docker/docker-compose.dev.yml down
	docker-compose -f docker/docker-compose.yml down
	docker system prune -f

# Utility commands
status: ## Show development status
	@echo "📊 Development Status:"
	@echo "====================="
	@echo ""
	@echo "🌐 Available URLs:"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "🔧 External Services Required:"
	@echo "PostgreSQL: Configure in DATABASE_URL"
	@echo "Redis: Configure in REDIS_URL"
	@echo ""
	@echo "📋 To check if services are running:"
	@echo "PostgreSQL: psql -U postgres -c 'SELECT version();'"
	@echo "Redis: redis-cli ping"
	@echo ""
	@echo "🐍 Poetry Status:"
	@cd apps/api && poetry env info

logs: ## Show application logs
	@echo "📋 Application logs..."
	pnpm dev 2>&1 | head -20

check-services: ## Check if external services are accessible
	@echo "🔍 Checking external services..."
	@echo "PostgreSQL: Testing connection..."
	@timeout 5 bash -c '</dev/tcp/localhost/5432' && echo "✅ PostgreSQL accessible" || echo "❌ PostgreSQL not accessible"
	@echo "Redis: Testing connection..."
	@timeout 5 bash -c '</dev/tcp/localhost/6379' && echo "✅ Redis accessible" || echo "❌ Redis not accessible"

check-deps: ## Check if all dependencies are installed
	@echo "🔍 Checking dependencies..."
	@echo "Node.js/pnpm:"
	@which node && echo "✅ Node.js installed" || echo "❌ Node.js not found"
	@which pnpm && echo "✅ pnpm installed" || echo "❌ pnpm not found"
	@echo "Python/Poetry:"
	@which python3 && echo "✅ Python installed" || echo "❌ Python not found"
	@which poetry && echo "✅ Poetry installed" || echo "❌ Poetry not found"

# Production commands
prod-build: ## Build for production
	@echo "🏭 Building for production..."
	NODE_ENV=production pnpm build
	cd apps/api && poetry build

prod-test: ## Run production tests
	@echo "🧪 Running production tests..."
	NODE_ENV=production pnpm test
	cd apps/api && poetry run pytest