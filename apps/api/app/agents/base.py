"""Base agent class for the agent system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str):
        """Initialize the agent.

        Args:
            name: The name of the agent
        """
        self.name = name
        self.memory: Dict[str, Any] = {}

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results.

        Args:
            input_data: Input data to process

        Returns:
            Processed results
        """
        pass

    def store_memory(self, key: str, value: Any) -> None:
        """Store information in agent memory.

        Args:
            key: Memory key
            value: Value to store
        """
        self.memory[key] = value

    def get_memory(self, key: str) -> Optional[Any]:
        """Retrieve information from agent memory.

        Args:
            key: Memory key

        Returns:
            Stored value or None
        """
        return self.memory.get(key)

    def clear_memory(self) -> None:
        """Clear agent memory."""
        self.memory.clear()
