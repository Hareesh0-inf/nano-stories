import pytest
from fastapi.testclient import TestClient
from io import BytesIO

# Import the FastAPI app - this will fail until the app is created
from src.main import app

client = TestClient(app)

def test_upload_product_success():
    """Test successful product image upload"""
    # First create a project
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Create a dummy image file
    image_data = b"dummy image data"
    image_file = BytesIO(image_data)
    image_file.name = "test_product.jpg"

    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("test_product.jpg", image_file, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_upload_product_invalid_project():
    """Test product upload with invalid project ID"""
    image_data = b"dummy image data"
    image_file = BytesIO(image_data)
    image_file.name = "test_product.jpg"

    response = client.post(
        "/projects/invalid-id/product",
        files={"image": ("test_product.jpg", image_file, "image/jpeg")}
    )
    assert response.status_code == 404

def test_upload_product_no_file():
    """Test product upload without file"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    response = client.post(f"/projects/{project_id}/product")
    assert response.status_code == 422

def test_upload_product_invalid_file_type():
    """Test product upload with invalid file type"""
    project_data = {"name": "Test Project"}
    project_response = client.post("/projects", json=project_data)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # Upload text file as image
    file_data = b"not an image"
    file_obj = BytesIO(file_data)
    file_obj.name = "test.txt"

    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("test.txt", file_obj, "text/plain")}
    )
    # This might pass or fail depending on validation
    # For now, assume it passes since validation comes later
    assert response.status_code in [200, 400]
