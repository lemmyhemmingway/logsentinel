from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AgentConfig(BaseModel):
    """Base configuration for all agents."""

    name: str
    enabled: bool = True
    parser_type: str
    metadata: dict[str, Any] = {}


class FileAgentConfig(AgentConfig):
    """Configuration specific to FileAgent."""

    file_path: str
    poll_interval: float = 1.0  # seconds
    read_from_end: bool = True


class BaseAgent(ABC):
    """Abstract base class for all LogSentinel agents."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self._running = False

    @abstractmethod
    def start(self):
        """Start the agent's execution."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the agent's execution."""
        pass

    @property
    def is_running(self) -> bool:
        """Check if the agent is currently running."""
        return self._running

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Return the current status of the agent."""
        pass
