import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_generate_character_success():
    """Test successful character generation"""
    # First create a project
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    character_data = {
        "details": "A young professional in business attire",
        "personality": "Confident and approachable"
    }

    response = client.post(f"/projects/{project_id}/character", json=character_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "image_url" in data
    assert isinstance(data["image_url"], str)

def test_generate_character_invalid_project():
    """Test character generation with invalid project ID"""
    character_data = {
        "details": "Test character",
        "personality": "Test personality"
    }

    response = client.post("/projects/invalid-id/character", json=character_data)
    assert response.status_code == 404

def test_generate_character_missing_data():
    """Test character generation with missing data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Missing details
    response = client.post(f"/projects/{project_id}/character", json={"personality": "Test"})
    assert response.status_code == 422

    # Missing personality
    response = client.post(f"/projects/{project_id}/character", json={"details": "Test"})
    assert response.status_code == 422

def test_generate_character_empty_data():
    """Test character generation with empty data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    character_data = {
        "details": "",
        "personality": ""
    }

    response = client.post(f"/projects/{project_id}/character", json=character_data)
    assert response.status_code == 422
