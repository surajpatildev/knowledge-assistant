"""FastAPI main application module."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.endpoints import chat, data_sources, health
from app.api.websocket import websocket_endpoint
from app.core.config import settings
from app.core.llm_factory import LLMFactory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("🚀 Starting Data Lens API...")

    # Initialize LLM Factory
    try:
        app.state.llm_factory = LLMFactory(settings.LLM_CONFIG)
        logger.success("✅ LLM Factory initialized successfully")
        logger.info(f"📋 Available providers: {app.state.llm_factory.get_available_providers()}")
        logger.info(f"🔧 Specialized tasks: {app.state.llm_factory.get_specialized_tasks()}")
    except Exception as e:
        logger.error(f"❌ Failed to initialize LLM Factory: {e}")
        # Continue without LLM Factory for now
        app.state.llm_factory = None

    # TODO: Initialize other services
    # app.state.orchestrator = OrchestratorAgent(app.state.llm_factory)

    yield

    # Shutdown
    logger.info("📴 Shutting down Data Lens API...")
    # Cleanup resources here


def create_app() -> FastAPI:
    """Create FastAPI application instance."""
    app = FastAPI(
        title="Data Lens API",
        description="Enterprise Knowledge Assistant Backend",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(data_sources.router, prefix="/api/data-sources", tags=["data"])

    # WebSocket endpoint
    app.websocket("/ws")(websocket_endpoint)

    return app


app = create_app()


def main() -> None:
    """Run the application with uvicorn."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )


if __name__ == "__main__":
    main()
