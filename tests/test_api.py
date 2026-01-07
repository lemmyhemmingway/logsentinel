from fastapi.testclient import TestClient

from src.api.main import app

# Create a test client using the FastAPI app instance
client = TestClient(app)

# Sample Data
VALID_LOG = '192.168.1.10 - - [07/Jan/2026:12:00:00 +0000] "GET /home HTTP/1.1" 200 1024'
INVALID_LOG = "This line is definitely not a log format"


def test_health_check():
    """
    Scenario: Check system health.
    Expectation: 200 OK and status active.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}


def test_parse_single_log_success():
    """
    Scenario: Send a valid log line to /parse/nginx.
    Expectation: 200 OK and valid JSON response.
    """
    payload = {"raw_log": VALID_LOG}

    # Notice: parser_type is in the URL path now
    response = client.post("/parse/nginx", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["source_ip"] == "192.168.1.10"
    assert data["status_code"] == 200


def test_parse_single_log_invalid_format():
    """
    Scenario: Send a malformed log line.
    Expectation: 422 Unprocessable Entity (Validation failed).
    """
    payload = {"raw_log": INVALID_LOG}

    response = client.post("/parse/nginx", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_parse_invalid_parser_type():
    """
    Scenario: Request a parser that does not exist (e.g., 'apache').
    Expectation: 400 Bad Request (Configuration Error).
    """
    payload = {"raw_log": VALID_LOG}

    response = client.post("/parse/apache", json=payload)

    assert response.status_code == 400
    assert "Invalid parser type" in response.json()["detail"]


def test_batch_processing_mixed_logs():
    """
    Scenario: Send a list containing 1 valid and 1 invalid log.
    Expectation: 200 OK. The result list should contain ONLY the valid log (size 1).
    """
    payload = {
        "raw_logs": [
            VALID_LOG,  # Should be parsed
            INVALID_LOG,  # Should be skipped
            VALID_LOG,  # Should be parsed
        ]
    }

    response = client.post("/parse/nginx/batch", json=payload)

    assert response.status_code == 200

    results = response.json()
    assert isinstance(results, list)
    assert len(results) == 2  # 3 logs sent, 1 invalid skipped -> 2 remained
    assert results[0]["source_ip"] == "192.168.1.10"
