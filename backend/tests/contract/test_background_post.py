import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_generate_background_success():
    """Test successful background generation"""
    # First create a project
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    background_data = {
        "scene_details": "Modern office environment with natural lighting",
        "lighting": "Soft morning light through large windows"
    }

    response = client.post(f"/projects/{project_id}/background", json=background_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "image_url" in data
    assert isinstance(data["image_url"], str)

def test_generate_background_invalid_project():
    """Test background generation with invalid project ID"""
    background_data = {
        "scene_details": "Test scene",
        "lighting": "Test lighting"
    }

    response = client.post("/projects/invalid-id/background", json=background_data)
    assert response.status_code == 404

def test_generate_background_missing_data():
    """Test background generation with missing data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Missing scene_details
    response = client.post(f"/projects/{project_id}/background", json={"lighting": "Test"})
    assert response.status_code == 422

    # Missing lighting
    response = client.post(f"/projects/{project_id}/background", json={"scene_details": "Test"})
    assert response.status_code == 422

def test_generate_background_empty_data():
    """Test background generation with empty data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    background_data = {
        "scene_details": "",
        "lighting": ""
    }

    response = client.post(f"/projects/{project_id}/background", json=background_data)
    assert response.status_code == 422
