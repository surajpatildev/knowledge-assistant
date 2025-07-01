"""Health check endpoints."""

from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "data-lens-api"}


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Dict[str, str]]:
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "database": "healthy",  # TODO: Add actual database check
            "redis": "healthy",     # TODO: Add actual Redis check
            "llm": "healthy",       # TODO: Add LLM provider check
        },
        "version": "1.0.0",
    }