import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from backend.src.main import app

client = TestClient(app)

def test_background_generation_workflow():
    """Test complete background generation workflow"""

    # Create project
    project_data = {"name": "Background Generation Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Generate background
    background_data = {
        "scene_details": "Modern corporate office with floor-to-ceiling windows overlooking city skyline",
        "lighting": "Natural daylight with soft shadows and warm afternoon glow"
    }
    response = client.post(f"/projects/{project_id}/background", json=background_data)
    assert response.status_code == 200
    background = response.json()
    assert "id" in background
    assert "image_url" in background

def test_background_with_different_scenes():
    """Test background generation with various scene types"""

    project_data = {"name": "Scene Variations Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    scenes = [
        {
            "scene_details": "Cozy coffee shop with warm lighting",
            "lighting": "Soft incandescent bulbs"
        },
        {
            "scene_details": "Outdoor park with trees and benches",
            "lighting": "Golden hour sunlight"
        },
        {
            "scene_details": "High-tech laboratory with equipment",
            "lighting": "Clinical fluorescent lighting"
        },
        {
            "scene_details": "Rustic workshop with wooden tools",
            "lighting": "Warm workshop lamps"
        }
    ]

    for scene in scenes:
        response = client.post(f"/projects/{project_id}/background", json=scene)
        assert response.status_code == 200
        background = response.json()
        assert "image_url" in background

def test_background_lighting_variations():
    """Test background generation with different lighting conditions"""

    project_data = {"name": "Lighting Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    lighting_scenarios = [
        "Bright studio lighting with softboxes",
        "Dramatic chiaroscuro with strong shadows",
        "Neon nightclub lighting with colored gels",
        "Candlelit intimate setting",
        "Harsh fluorescent office lighting",
        "Magical moonlight with blue tones"
    ]

    for lighting in lighting_scenarios:
        background_data = {
            "scene_details": "Generic business setting",
            "lighting": lighting
        }
        response = client.post(f"/projects/{project_id}/background", json=background_data)
        assert response.status_code == 200
        background = response.json()
        assert "image_url" in background

def test_background_regeneration():
    """Test background regeneration with different parameters"""

    project_data = {"name": "Background Regeneration Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Generate first background
    background_data1 = {
        "scene_details": "Simple office",
        "lighting": "Basic lighting"
    }
    response1 = client.post(f"/projects/{project_id}/background", json=background_data1)
    assert response1.status_code == 200
    background1 = response1.json()

    # Generate second background with different parameters
    background_data2 = {
        "scene_details": "Luxury executive office with city view",
        "lighting": "Premium lighting setup"
    }
    response2 = client.post(f"/projects/{project_id}/background", json=background_data2)
    assert response2.status_code == 200
    background2 = response2.json()

    # Should have different IDs
    assert background1["id"] != background2["id"]

def test_background_validation_edge_cases():
    """Test background generation with edge case inputs"""

    project_data = {"name": "Background Edge Cases"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Very detailed scene description
    detailed_scene = "A " + "highly detailed " * 50 + "scene description"
    background_data = {
        "scene_details": detailed_scene,
        "lighting": "Complex lighting setup"
    }
    response = client.post(f"/projects/{project_id}/background", json=background_data)
    assert response.status_code in [200, 400, 422]

    # Minimal description
    minimal_data = {
        "scene_details": "Office",
        "lighting": "Light"
    }
    response = client.post(f"/projects/{project_id}/background", json=minimal_data)
    assert response.status_code in [200, 400, 422]

def test_background_without_project():
    """Test background generation on non-existent projects"""

    background_data = {
        "scene_details": "Test scene",
        "lighting": "Test lighting"
    }

    response = client.post("/projects/invalid-id/background", json=background_data)
    assert response.status_code == 404
