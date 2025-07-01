"""WebSocket handlers for real-time communication."""

import json
import logging
from typing import Any, Dict

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"Client {session_id} connected")

    def disconnect(self, session_id: str):
        """Remove WebSocket connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"Client {session_id} disconnected")

    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to specific client."""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_json(message)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    session_id = websocket.headers.get("x-session-id", "default")
    await manager.connect(websocket, session_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message["type"] == "query":
                # TODO: Process query with orchestrator streaming
                await websocket.send_json({"type": "thinking", "content": "Processing your query..."})

                # Simulate processing
                await websocket.send_json(
                    {
                        "type": "complete",
                        "data": {"query": message["query"]},
                        "ui": [],
                        "suggestions": ["Ask another question"],
                    }
                )

            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {str(e)}")
        await websocket.send_json({"type": "error", "message": str(e)})
        manager.disconnect(session_id)
