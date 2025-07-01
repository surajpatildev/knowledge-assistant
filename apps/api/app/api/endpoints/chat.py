"""Chat endpoints for query processing."""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    """Chat query request model."""

    query: str
    session_id: str = "default"
    stream: bool = False


class QueryResponse(BaseModel):
    """Chat query response model."""

    success: bool
    message: str
    data: Dict[str, Any] = {}
    ui_components: list = []
    suggestions: list = []


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> QueryResponse:
    """Process a chat query and return results."""
    try:
        # TODO: Implement actual query processing with orchestrator
        return QueryResponse(
            success=True,
            message=f"Processed query: {request.query}",
            data={"query": request.query, "session_id": request.session_id},
            suggestions=[
                "Try asking about data trends",
                "Show me a chart",
                "Export to CSV",
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/history")
async def get_chat_history(session_id: str) -> Dict[str, Any]:
    """Get chat history for a session."""
    # TODO: Implement actual history retrieval
    return {"session_id": session_id, "messages": [], "total": 0}


@router.get("/llm/test")
async def test_llm_factory(app_request: Request) -> Dict[str, Any]:
    """Test endpoint to demonstrate LLM Factory capabilities."""
    llm_factory = getattr(app_request.app.state, "llm_factory", None)

    if llm_factory is None:
        return {
            "success": False,
            "message": "LLM Factory not initialized. Please check your API keys.",
            "providers": [],
            "specialized_tasks": [],
        }

    try:
        # Test basic completion
        test_prompt = "Explain what a data warehouse is in one sentence."
        response = await llm_factory.get_completion(prompt=test_prompt, temperature=0.3, max_tokens=100)

        return {
            "success": True,
            "message": "LLM Factory is working correctly",
            "test_response": response,
            "providers": llm_factory.get_available_providers(),
            "specialized_tasks": llm_factory.get_specialized_tasks(),
            "provider_info": {
                task: llm_factory.get_provider_info(task) for task in llm_factory.get_specialized_tasks()
            },
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"LLM Factory test failed: {str(e)}",
            "providers": llm_factory.get_available_providers(),
            "specialized_tasks": llm_factory.get_specialized_tasks(),
        }
