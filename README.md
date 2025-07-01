# Data Lens - Enterprise Knowledge Assistant

A conversational AI platform that enables users to interact with their data through natural language. Built with a multi-agent architecture using Next.js frontend and FastAPI backend.

## 🏗️ Architecture

```
data-lens/
├── apps/
│   ├── web/                    # Next.js frontend application
│   └── api/                    # FastAPI backend service
├── packages/
│   ├── shared-types/           # TypeScript type definitions
│   ├── ui-components/          # Reusable React components
│   └── eslint-config/          # Shared ESLint configuration
├── docker/                     # Docker configurations (optional)
├── scripts/                    # Development scripts
└── docs/                       # Documentation
```

## ✨ Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Multi-Agent System**: Specialized agents for SQL generation, data analysis, and UI creation
- **Dynamic Visualizations**: Automatically generated charts and dashboards
- **Multi-Source Integration**: Connect to databases, APIs, and files
- **Real-time Streaming**: WebSocket-based real-time query processing
- **Monorepo Architecture**: Shared types and components between frontend and backend

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://python.org/))
- **pnpm** (will be installed automatically)
- **Poetry** - Python dependency management ([Install](https://python-poetry.org/docs/#installation))
- **PostgreSQL** - External installation required
- **Redis** - External installation required

### External Services Setup

**Important**: This project requires external PostgreSQL and Redis services. Ensure they are running before starting development.

#### PostgreSQL Setup
```bash
# Your PostgreSQL should be accessible at:
# Default: postgresql://postgres:password@localhost:5432/data_lens

# Create database
createdb data_lens

# Initialize schema
psql -U postgres -d data_lens -f docker/init-db/01-init.sql
```

#### Redis Setup
```bash
# Your Redis should be accessible at:
# Default: redis://localhost:6379

# Test Redis connection
redis-cli ping
```

### Automatic Setup

Run the setup script for automatic configuration:

```bash
# Clone/navigate to the project
cd data-lens

# Run setup script (checks external services and installs Poetry if needed)
./scripts/setup.sh
```

### Manual Setup

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies:**
   ```bash
   # JavaScript dependencies
   pnpm install
   
   # Python dependencies with Poetry
   cd apps/api && poetry install
   ```

3. **Set up environment variables:**
   ```bash
   # Copy environment files
   cp .env.example .env
   cp apps/web/.env.local.example apps/web/.env.local
   
   # Edit .env with your external service URLs
   # Update DATABASE_URL and REDIS_URL to match your installations
   ```

4. **Initialize database:**
   ```bash
   # Connect to your PostgreSQL and run:
   psql -U postgres -d data_lens -f docker/init-db/01-init.sql
   ```

5. **Start development servers:**
   ```bash
   make dev
   # or
   pnpm dev
   ```

## 🛠️ Development

### Available Commands

```bash
# Development
make dev              # Start all development servers
make dev-api          # Start only API server (with Poetry)
make dev-web          # Start only web server

# Service Checks
make check-services   # Test external service connectivity
make check-deps       # Verify all tools (Node.js, pnpm, Python, Poetry)
make status           # Show development status

# Building
make build            # Build all packages
make build-api        # Build API with Poetry
make build-web        # Build web only

# Testing
make test             # Run all tests
make test-api         # Run API tests with Poetry
make test-web         # Run web tests

# Code Quality
make lint             # Run linters (JS + Python)
make format           # Format code (JS + Python)
make type-check       # TypeScript + mypy type checking

# Poetry-Specific Commands
make poetry-install   # Install Python dependencies
make poetry-add       # Add new package (e.g., make poetry-add PACKAGE=requests)
make poetry-add-dev   # Add dev package
make poetry-show      # Show dependency tree
make poetry-lock      # Update lock file
make poetry-shell     # Enter Poetry virtual environment

# Database
make db-init          # Show database initialization instructions
make db-migrate       # Run Alembic migrations
make db-migration     # Create new migration

# Utilities
make clean            # Clean build artifacts
make help             # Show all commands
```

### Python Development with Poetry

#### Virtual Environment Management
```bash
# Poetry automatically manages virtual environments
cd apps/api

# Install dependencies
poetry install

# Add new dependencies
poetry add requests
poetry add --group dev pytest

# Enter Poetry shell (virtual environment)
poetry shell

# Run commands in Poetry environment
poetry run python -m app.main
poetry run pytest
poetry run black .
```

#### Dependency Management
```bash
# Show installed packages
poetry show

# Show dependency tree
poetry show --tree

# Update dependencies
poetry update

# Generate lock file
poetry lock
```

### External Service Configuration

#### Environment Variables

Update `.env` with your external service configuration:

```bash
# Database - Your external PostgreSQL
DATABASE_URL=postgresql://username:password@your-host:5432/database_name

# Redis - Your external Redis
REDIS_URL=redis://your-host:6379/0

# LLM Providers
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### Service Verification

```bash
# Check if external services are accessible
make check-services

# Manual checks
psql -U postgres -c 'SELECT version();'  # PostgreSQL
redis-cli ping                            # Redis
poetry --version                          # Poetry
```

### Project Structure

#### Backend (FastAPI + Poetry)
```
apps/api/
├── app/
│   ├── main.py               # FastAPI application
│   ├── core/                 # Core configuration and services
│   ├── agents/               # Agent system
│   ├── api/                  # API endpoints
│   ├── models/               # Data models
│   ├── services/             # Business logic
│   └── tools/                # Agent tools
├── pyproject.toml            # Poetry dependencies and config
├── poetry.lock               # Lock file for reproducible builds
└── Dockerfile               # Multi-stage container build
```

#### Frontend (Next.js + pnpm)
```
apps/web/
├── app/                      # Next.js App Router
├── components/               # React components
├── lib/                      # Utilities and configurations
├── hooks/                    # React hooks
├── package.json              # pnpm dependencies
└── Dockerfile.dev            # Development container
```

## 🐳 Docker (Optional)

Docker configurations are available for containerized development, but external PostgreSQL and Redis are still required.

### Containerized Development (Optional)
```bash
# Start API in Docker (connects to external services)
make docker-api

# Start Web in Docker
make docker-web

# Stop containers
make docker-down
```

The Dockerfiles use multi-stage builds with Poetry for efficient container images.

## 🔧 Configuration

### LLM Configuration

The system supports multiple LLM providers with intelligent routing:

- **Primary**: OpenAI GPT-4 for complex reasoning
- **Fallback**: Anthropic Claude 3 for alternative processing
- **Specialized**: Different models for specific tasks

Configure in `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Poetry Configuration

Poetry settings in `pyproject.toml`:
```toml
[tool.poetry]
name = "data-lens-api"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
# ... other dependencies

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.9.0"
# ... dev dependencies
```

## 🧪 Testing

### Backend Tests (Poetry)
```bash
cd apps/api
poetry run pytest

# With coverage
poetry run pytest --cov=app

# Run specific tests
poetry run pytest tests/test_agents.py
```

### Frontend Tests (pnpm)
```bash
cd apps/web
pnpm test
```

## 📊 Monitoring

### Health Checks
- **API Health**: `http://localhost:8000/api/health`
- **Detailed Health**: `http://localhost:8000/api/health/detailed`

### Development URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### External Services
- **PostgreSQL**: Configure in DATABASE_URL
- **Redis**: Configure in REDIS_URL

## 🏛️ Agent System

The application uses a multi-agent architecture:

1. **Orchestrator Agent**: Coordinates the entire workflow
2. **Router Agent**: Classifies user intents and routes queries
3. **SQL Agent**: Generates and executes SQL queries
4. **Analysis Agent**: Performs data analysis and generates insights
5. **UI Agent**: Creates dynamic visualizations and components

## 🔌 Data Sources

Supported data source types:
- **PostgreSQL** - Primary database connections
- **MySQL** - Alternative database support
- **CSV Files** - File-based data import
- **REST APIs** - External API integration
- **JSON Files** - Structured data files

## 🚢 Deployment

### Production Build
```bash
make prod-build
```

### Docker Production
```bash
# Requires external PostgreSQL and Redis
docker-compose -f docker/docker-compose.yml up -d
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Development Workflow
```bash
# Start development (requires external services)
make setup
make dev

# Make changes and test
make lint
make test
make type-check

# Add new Python dependency
make poetry-add PACKAGE=package-name

# Build and verify
make build
```

## 🐛 Troubleshooting

### Common Issues

1. **External service connectivity**: 
   - Run `make check-services` to verify PostgreSQL and Redis
   - Update DATABASE_URL and REDIS_URL in .env if needed

2. **Poetry not found**: 
   - Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
   - Restart terminal and try again

3. **Port conflicts**: Ensure ports 3000, 8000 are available

4. **Dependencies**: Run `make check-deps` to verify all tools

### Service Checks

```bash
make check-services     # Test external service connectivity
make check-deps         # Verify tools (Node.js, pnpm, Python, Poetry)
make status            # Show service status
make logs              # Show application logs

# Manual service checks
psql -U postgres -c 'SELECT version();'  # PostgreSQL
redis-cli ping                            # Redis
poetry --version                          # Poetry
```

### Poetry Troubleshooting

```bash
# Check Poetry environment
cd apps/api
poetry env info

# Reinstall dependencies
poetry install --no-cache

# Clear Poetry cache
poetry cache clear --all pypi
```

### External Service Setup

If you need to set up PostgreSQL and Redis externally:

#### PostgreSQL
```bash
# Install PostgreSQL (example for macOS)
brew install postgresql
brew services start postgresql

# Create database and user
createdb data_lens
psql -d data_lens -f docker/init-db/01-init.sql
```

#### Redis
```bash
# Install Redis (example for macOS)
brew install redis
brew services start redis

# Test
redis-cli ping
```

## 📚 Documentation

- [Architecture Overview](./docs/architecture.md)
- [Agent System Guide](./docs/agents.md)
- [API Reference](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Poetry for Python dependency management
- Uses pnpm for JavaScript package management
- Powered by OpenAI GPT-4 and Anthropic Claude
- Built on FastAPI, Next.js, and modern web technologies

---

**Version**: 1.0.0  
**Status**: Development  
**Dependencies**: Poetry (Python) + pnpm (JavaScript)  
**External Services**: PostgreSQL & Redis required  
**Last Updated**: 2024-01-01