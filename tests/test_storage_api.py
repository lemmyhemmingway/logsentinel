import os

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.storage import LogStorage

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_storage():
    # Use a test database
    db_path = "test_logs.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Override storage in routes (hacky for this structure but works)
    from src.api import routes

    routes.storage = LogStorage(db_path=db_path)

    yield

    if os.path.exists(db_path):
        os.remove(db_path)


def test_parse_and_persist():
    # 1. Post a log
    response = client.post(
        "/parse/nginx",
        json={"raw_log": '192.168.1.1 - - [07/Jan/2026:14:30:00 +0300] "GET /test HTTP/1.1" 200 1024'},
    )
    assert response.status_code == 200

    # 2. Check if it's in /logs
    response = client.get("/logs")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1
    assert logs[0]["source_ip"] == "192.168.1.1"
    assert logs[0]["service_name"] == "nginx-access"


def test_batch_persist():
    # 1. Post batch logs
    response = client.post(
        "/parse/nginx/batch",
        json={
            "raw_logs": [
                '192.168.1.1 - - [07/Jan/2026:14:30:00 +0300] "GET /1 HTTP/1.1" 200 1024',
                '192.168.1.2 - - [07/Jan/2026:14:30:01 +0300] "GET /2 HTTP/1.1" 404 512',
            ]
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    # 2. Check stats
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_logs"] == 2
    assert stats["services"]["nginx-access"] == 2


def test_get_logs_filtering():
    client.post(
        "/parse/nginx", json={"raw_log": '1.1.1.1 - - [07/Jan/2026:14:30:00 +0300] "GET / HTTP/1.1" 200 0'}
    )

    response = client.get("/logs?service=nginx-access")
    assert len(response.json()) == 1

    response = client.get("/logs?service=apache")
    assert len(response.json()) == 0
