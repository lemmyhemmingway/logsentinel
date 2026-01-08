from typing import Any

from src.agents.base import AgentConfig, BaseAgent, FileAgentConfig
from src.agents.file_agent import FileAgent
from src.exceptions import ConfigurationError


class AgentFactory:
    """
    Factory for creating agents based on configuration.
    """

    _agent_map: dict[str, type[BaseAgent]] = {
        "file": FileAgent,
    }

    _config_map: dict[str, type[AgentConfig]] = {
        "file": FileAgentConfig,
    }

    @classmethod
    def create_agent(cls, agent_type: str, config_dict: dict[str, Any], **kwargs: Any) -> BaseAgent:
        """
        Creates an agent instance based on the type and configuration.
        """
        agent_class = cls._agent_map.get(agent_type)
        config_class = cls._config_map.get(agent_type)

        if not agent_class or not config_class:
            raise ConfigurationError(f"Unsupported agent type: {agent_type}")

        try:
            config = config_class(**config_dict)
            return agent_class(config, **kwargs)
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize agent '{agent_type}': {e}") from e
