import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_create_project_success():
    """Test successful project creation"""
    project_data = {
        "name": "Test Brand Story Project"
    }

    response = client.post("/projects", json=project_data)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == project_data["name"]
    assert "created_at" in data

def test_create_project_invalid_data():
    """Test project creation with invalid data"""
    # Empty name
    response = client.post("/projects", json={"name": ""})
    assert response.status_code == 422

    # Missing name
    response = client.post("/projects", json={})
    assert response.status_code == 422

def test_create_project_duplicate_name():
    """Test project creation with duplicate name"""
    project_data = {
        "name": "Duplicate Project"
    }

    # Create first project
    response1 = client.post("/projects", json=project_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/projects", json=project_data)
    # This might be allowed or not depending on business rules
    # For now, assume it's allowed
    assert response2.status_code == 201
