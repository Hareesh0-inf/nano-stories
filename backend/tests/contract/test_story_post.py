import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_set_story_success():
    """Test successful story setting"""
    # First create a project
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    story_data = {
        "story_text": "A compelling brand story about innovation and customer success"
    }

    response = client.post(f"/projects/{project_id}/story", json=story_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_set_story_invalid_project():
    """Test story setting with invalid project ID"""
    story_data = {
        "story_text": "Test story"
    }

    response = client.post("/projects/invalid-id/story", json=story_data)
    assert response.status_code == 404

def test_set_story_missing_data():
    """Test story setting with missing data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Missing story_text
    response = client.post(f"/projects/{project_id}/story", json={})
    assert response.status_code == 422

def test_set_story_empty_data():
    """Test story setting with empty data"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    story_data = {
        "story_text": ""
    }

    response = client.post(f"/projects/{project_id}/story", json=story_data)
    assert response.status_code == 422
