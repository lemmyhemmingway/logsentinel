from unittest.mock import MagicMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from src.agents import AgentFactory, FileAgent, FileAgentConfig, LogSentinelClient
from src.api.main import app
from src.exceptions import ConfigurationError

# Test Constants
BASE_URL = "http://testserver"
PARSER_TYPE = "nginx"
VALID_LOG = '192.168.1.10 - - [07/Jan/2026:12:00:00 +0000] "GET /home HTTP/1.1" 200 1024'

# --- Unit Tests for AgentFactory ---


def test_agent_factory_create_file_agent():
    config_dict = {"name": "test-file-agent", "type": "file", "parser_type": "nginx", "file_path": "test.log"}
    agent = AgentFactory.create_agent("file", config_dict)
    assert isinstance(agent, FileAgent)
    assert agent.config.name == "test-file-agent"
    assert agent.config.file_path == "test.log"


def test_agent_factory_invalid_type():
    with pytest.raises(ConfigurationError):
        AgentFactory.create_agent("invalid", {"name": "test"})


# --- Unit Tests for LogSentinelClient ---


@patch("httpx.Client.post")
def test_client_send_log(mock_post):
    mock_post.return_value = MagicMock(spec=httpx.Response, status_code=200)
    mock_post.return_value.json.return_value = {"status": "success"}

    client = LogSentinelClient(BASE_URL)
    result = client.send_log(PARSER_TYPE, VALID_LOG)

    assert result == {"status": "success"}
    mock_post.assert_called_once()


@patch("httpx.Client.post")
def test_client_send_batch(mock_post):
    mock_post.return_value = MagicMock(spec=httpx.Response, status_code=200)
    mock_post.return_value.json.return_value = [{"status": "success"}]

    client = LogSentinelClient(BASE_URL)
    result = client.send_batch(PARSER_TYPE, [VALID_LOG])

    assert result == [{"status": "success"}]
    mock_post.assert_called_once()


# --- Unit Tests for FileAgent ---


def test_file_agent_tailing(tmp_path):
    log_file = tmp_path / "access.log"
    log_file.write_text("")

    received_lines = []

    def callback(line):
        received_lines.append(line)

    config = FileAgentConfig(
        name="test-tail", parser_type="nginx", file_path=str(log_file), poll_interval=0.1, read_from_end=False
    )

    agent = FileAgent(config, on_line_received=callback)

    # We'll manually call _poll instead of start() to avoid the while loop in tests
    agent._poll()
    assert len(received_lines) == 0

    # Add a line
    log_file.write_text(VALID_LOG + "\n")
    agent._poll()
    assert len(received_lines) == 1
    assert received_lines[0] == VALID_LOG


# --- Integration Test ---


def test_agent_to_api_integration(tmp_path):
    # This test simulates the whole flow: File -> FileAgent -> Client -> FastAPI
    log_file = tmp_path / "integration.log"
    log_file.write_text("")

    # FastAPI TestClient
    api_client = TestClient(app)

    ls_client = LogSentinelClient(BASE_URL)

    # Mocking the client's send_log method to call our TestClient instead of actual HTTP
    responses = []
    with patch.object(ls_client, "send_log") as mock_send_log:

        def side_effect(parser_type, raw_log):
            res = api_client.post(f"/parse/{parser_type}", json={"raw_log": raw_log})
            responses.append(res)
            return res

        mock_send_log.side_effect = side_effect

        config = FileAgentConfig(
            name="integration-agent",
            parser_type="nginx",
            file_path=str(log_file),
            poll_interval=0.1,
            read_from_end=False,
        )

        agent = FileAgent(config, on_line_received=lambda line: ls_client.send_log(config.parser_type, line))

        # 1. Start with empty file
        agent._poll()
        assert mock_send_log.call_count == 0

        # 2. Append a valid log
        with open(log_file, "a") as f:
            f.write(VALID_LOG + "\n")

        agent._poll()

        assert mock_send_log.call_count == 1

        # Verify the API response (captured in responses list)
        assert len(responses) == 1
        response = responses[0]
        assert response.status_code == 200
        assert response.json()["source_ip"] == "192.168.1.10"
