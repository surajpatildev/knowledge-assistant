# Data Lens API

FastAPI backend service for the Data Lens Enterprise Knowledge Assistant.

## Development

This API is part of the Data Lens monorepo. See the main [README](../../README.md) for setup instructions.

## Running

```bash
# From the monorepo root
make dev-api

# Or directly with Poetry
cd apps/api
poetry run uvicorn app.main:app --reload
```

## Features

- Multi-agent AI architecture
- FastAPI with async/await
- SQLAlchemy ORM with PostgreSQL
- Redis for caching
- LangChain integration
- OpenAI and Anthropic LLM support