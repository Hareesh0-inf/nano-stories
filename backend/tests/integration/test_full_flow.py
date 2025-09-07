import pytest
from fastapi.testclient import TestClient
from io import BytesIO

# Import the FastAPI app - this will fail until the app is created
from backend.src.main import app

client = TestClient(app)

def test_full_brand_storytelling_workflow():
    """Test the complete brand storytelling workflow from start to finish"""

    # Step 1: Create a new project
    project_data = {
        "name": "Complete Brand Story Project"
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project = response.json()
    project_id = project["id"]

    # Step 2: Generate character
    character_data = {
        "details": "A confident young entrepreneur in professional attire",
        "personality": "Innovative, approachable, and trustworthy"
    }
    response = client.post(f"/projects/{project_id}/character", json=character_data)
    assert response.status_code == 200
    character = response.json()
    assert "image_url" in character

    # Step 3: Upload product image
    image_data = b"fake product image data"
    image_file = BytesIO(image_data)
    image_file.name = "product_logo.png"
    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("product_logo.png", image_file, "image/png")}
    )
    assert response.status_code == 200

    # Step 4: Generate background
    background_data = {
        "scene_details": "Modern office with large windows and city skyline view",
        "lighting": "Natural soft lighting with golden hour warmth"
    }
    response = client.post(f"/projects/{project_id}/background", json=background_data)
    assert response.status_code == 200
    background = response.json()
    assert "image_url" in background

    # Step 5: Set story
    story_data = {
        "story_text": "From humble beginnings to industry leader, our journey is one of innovation, perseverance, and customer-centric excellence. We started with a simple idea and built something extraordinary."
    }
    response = client.post(f"/projects/{project_id}/story", json=story_data)
    assert response.status_code == 200

    # Step 6: Generate final images
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 200
    images = response.json()
    assert isinstance(images, list)
    assert len(images) == 3
    for image in images:
        assert "id" in image
        assert "prompt" in image
        assert "image_url" in image

def test_workflow_with_multiple_iterations():
    """Test workflow with character regeneration and approval flow"""

    # Create project
    project_data = {"name": "Iterative Project"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Generate initial character
    character_data = {
        "details": "Business professional",
        "personality": "Confident"
    }
    response = client.post(f"/projects/{project_id}/character", json=character_data)
    assert response.status_code == 200

    # Simulate user not approving - regenerate with different details
    new_character_data = {
        "details": "Young entrepreneur with modern style",
        "personality": "Dynamic and inspiring"
    }
    response = client.post(f"/projects/{project_id}/character", json=new_character_data)
    assert response.status_code == 200

    # Continue with rest of workflow
    # Upload product
    image_data = b"product image"
    image_file = BytesIO(image_data)
    image_file.name = "product.jpg"
    client.post(
        f"/projects/{project_id}/product",
        files={"image": ("product.jpg", image_file, "image/jpeg")}
    )

    # Generate background
    background_data = {
        "scene_details": "Contemporary workspace",
        "lighting": "Bright and modern"
    }
    client.post(f"/projects/{project_id}/background", json=background_data)

    # Set story
    story_data = {"story_text": "Innovation drives our success"}
    client.post(f"/projects/{project_id}/story", json=story_data)

    # Generate images
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 200

def test_workflow_error_recovery():
    """Test error handling and recovery in the workflow"""

    # Create project
    project_data = {"name": "Error Recovery Project"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Try to generate images without required components
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 400  # Should fail

    # Add components one by one
    character_data = {"details": "Test", "personality": "Test"}
    client.post(f"/projects/{project_id}/character", json=character_data)

    # Still incomplete
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 400

    # Add product
    image_data = b"image"
    image_file = BytesIO(image_data)
    image_file.name = "test.jpg"
    client.post(
        f"/projects/{project_id}/product",
        files={"image": ("test.jpg", image_file, "image/jpeg")}
    )

    # Still incomplete
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 400

    # Add background
    background_data = {"scene_details": "Test", "lighting": "Test"}
    client.post(f"/projects/{project_id}/background", json=background_data)

    # Still incomplete
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 400

    # Add story
    story_data = {"story_text": "Test story"}
    client.post(f"/projects/{project_id}/story", json=story_data)

    # Now should work
    response = client.post(f"/projects/{project_id}/generate")
    assert response.status_code == 200
