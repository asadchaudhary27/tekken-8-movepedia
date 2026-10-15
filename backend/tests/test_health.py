import pytest
from fastapi import status


def test_health_check_endpoint(client):
    """Verifies backend startup and health check response."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "online"
    assert "Tekken" in data["app_name"]
    assert data["database"] == "connected"


def test_openapi_docs_endpoint(client):
    """Verifies that OpenAPI documentation is successfully exposed."""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "paths" in data
    assert "/api/v1/health" in data["paths"]
    assert "/api/v1/characters" in data["paths"]
    assert "/api/v1/notation/convert" in data["paths"]
