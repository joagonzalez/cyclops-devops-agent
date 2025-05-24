"""
Tests for health api endpoints.
"""
from fastapi.testclient import TestClient

from src import app

client = TestClient(app=app)


def test_read_main():
    """
    Test /health/status/ endpoint
    """
    response: TestClient = client.get("/health/status/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
