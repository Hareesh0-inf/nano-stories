import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app - this will fail until the app is created
from backend.src.main import app

client = TestClient(app)

def test_character_generation_and_approval_flow():
    """Test character generation with approval/rejection workflow"""

    # Create project
    project_data = {"name": "Character Approval Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Generate first character
    character_data = {
        "details": "Middle-aged business executive",
        "personality": "Serious and professional"
    }
    response = client.post(f"/projects/{project_id}/character", json=character_data)
    assert response.status_code == 200
    character1 = response.json()
    assert "image_url" in character1

    # Simulate user rejecting the character - generate new one
    # In a real app, this might be a separate approval endpoint
    # For now, just test that we can generate multiple characters
    new_character_data = {
        "details": "Young innovative entrepreneur",
        "personality": "Energetic and creative"
    }
    response = client.post(f"/projects/{project_id}/character", json=new_character_data)
    assert response.status_code == 200
    character2 = response.json()
    assert "image_url" in character2

    # Characters should be different (in real implementation)
    # For now, just check that both exist
    assert character1["id"] != character2["id"]

def test_character_with_different_personality_types():
    """Test character generation with various personality types"""

    project_data = {"name": "Personality Test Project"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    personalities = [
        "Confident and authoritative",
        "Warm and approachable",
        "Innovative and visionary",
        "Reliable and trustworthy"
    ]

    for personality in personalities:
        character_data = {
            "details": "Business professional",
            "personality": personality
        }
        response = client.post(f"/projects/{project_id}/character", json=character_data)
        assert response.status_code == 200
        character = response.json()
        assert "image_url" in character

def test_character_validation_edge_cases():
    """Test character generation with edge case inputs"""

    project_data = {"name": "Character Edge Cases"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Very long description
    long_description = "A " + "very " * 100 + "long description"
    character_data = {
        "details": long_description,
        "personality": "Test personality"
    }
    response = client.post(f"/projects/{project_id}/character", json=character_data)
    # Should either succeed or fail gracefully
    assert response.status_code in [200, 400, 422]

    # Special characters in description
    special_description = "Character with émojis 😀 and spëcial chärs"
    character_data = {
        "details": special_description,
        "personality": "Fun personality"
    }
    response = client.post(f"/projects/{project_id}/character", json=character_data)
    assert response.status_code in [200, 400, 422]

def test_character_generation_without_project():
    """Test character generation attempts on non-existent projects"""

    character_data = {
        "details": "Test character",
        "personality": "Test personality"
    }

    # Invalid UUID format
    response = client.post("/projects/not-a-uuid/character", json=character_data)
    assert response.status_code == 404

    # Non-existent valid UUID
    response = client.post("/projects/12345678-1234-5678-9012-123456789012/character", json=character_data)
    assert response.status_code == 404
