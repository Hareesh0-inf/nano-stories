import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_generate_images_success():
    """Test successful image generation"""
    # First create a project and add all required components
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Add character
    character_data = {
        "details": "Professional character",
        "personality": "Confident"
    }
    client.post(f"/projects/{project_id}/character", json=character_data)

    # Add product (dummy)
    from io import BytesIO
    image_data = b"dummy image data"
    image_file = BytesIO(image_data)
    image_file.name = "test_product.jpg"
    client.post(
        f"/projects/{project_id}/product",
        files={"image": ("test_product.jpg", image_file, "image/jpeg")}
    )

    # Add background
    background_data = {
        "scene_details": "Office setting",
        "lighting": "Natural light"
    }
    client.post(f"/projects/{project_id}/background", json=background_data)

    # Add story
    story_data = {
        "story_text": "Brand story about success"
    }
    client.post(f"/projects/{project_id}/story", json=story_data)

    # Now generate images
    response = client.post(f"/projects/{project_id}/generate")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3  # Should return 3 images
    for image in data:
        assert "id" in image
        assert "prompt" in image
        assert "image_url" in image

def test_generate_images_incomplete_project():
    """Test image generation with incomplete project"""
    project_data = {"name": "Incomplete Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Try to generate without required components
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 400

def test_generate_images_invalid_project():
    """Test image generation with invalid project ID"""
    response = client.post("/projects/invalid-id/generate")
    assert response.status_code == 404
