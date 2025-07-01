"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    class Config:
        from_attributes = True


class QueryRequest(BaseSchema):
    """Chat query request schema."""

    query: str = Field(..., description="User query")
    session_id: str = Field(default="default", description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional context"
    )


class QueryResponse(BaseSchema):
    """Chat query response schema."""

    success: bool = Field(..., description="Whether the query was successful")
    data: Dict[str, Any] = Field(default_factory=dict, description="Query results")
    ui_components: List[Dict[str, Any]] = Field(
        default_factory=list, description="UI components"
    )
    suggestions: List[str] = Field(
        default_factory=list, description="Follow-up suggestions"
    )
    error: Optional[str] = Field(default=None, description="Error message if any")


class DataSourceCreate(BaseSchema):
    """Data source creation schema."""

    name: str = Field(..., description="Data source name")
    type: str = Field(..., description="Data source type")
    connection_string: str = Field(..., description="Connection string")
    description: Optional[str] = Field(
        default="", description="Data source description"
    )


class DataSourceResponse(BaseSchema):
    """Data source response schema."""

    id: str = Field(..., description="Data source ID")
    name: str = Field(..., description="Data source name")
    type: str = Field(..., description="Data source type")
    description: str = Field(..., description="Data source description")
    status: str = Field(..., description="Data source status")
    created_at: datetime = Field(..., description="Creation timestamp")


class HealthResponse(BaseSchema):
    """Health check response schema."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: Optional[str] = Field(default=None, description="Service version")
