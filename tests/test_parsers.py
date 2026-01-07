from src.parsers.nginx import NginxParser

# Sample log lines for testing
VALID_LOG = '192.168.1.50 - - [07/Jan/2026:14:30:00 +0000] "GET /api/status HTTP/1.1" 200 1024'
BROKEN_LOG = "This is not a log line, just some random text"


def test_nginx_parser_valid_log():
    """
    Scenario: A valid Nginx log line is provided.
    Expectation: Should return a LogEntry object with correct IP, Status Code, and Message.
    """
    parser = NginxParser()
    result = parser.parse(VALID_LOG)

    assert result is not None, "Parser failed to process a valid log line (returned None)."
    assert result.source_ip == "192.168.1.50"
    assert result.status_code == 200
    assert result.message == "GET /api/status HTTP/1.1"

    # Date verification (Year, Month)
    assert result.timestamp.year == 2026
    assert result.timestamp.month == 1


def test_nginx_parser_broken_log():
    """
    Scenario: An invalid/malformed log line is provided.
    Expectation: Should return None (or handle gracefully depending on policy).
    """
    parser = NginxParser()
    result = parser.parse(BROKEN_LOG)

    assert result is None, "Parser should have returned None for a broken log line."


def test_nginx_parser_metadata():
    """
    Scenario: Verify if extra data (like bytes sent) is correctly stored in metadata.
    """
    parser = NginxParser()
    result = parser.parse(VALID_LOG)

    # In Phase 1, we decided to store 'bytes' in metadata
    assert "bytes" in result.metadata
    assert result.metadata["bytes"] == 1024
