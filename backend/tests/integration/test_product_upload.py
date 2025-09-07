import pytest
from fastapi.testclient import TestClient
from io import BytesIO

# Import the FastAPI app - this will fail until the app is created
from backend.src.main import app

client = TestClient(app)

def test_product_upload_workflow():
    """Test complete product upload and integration workflow"""

    # Create project
    project_data = {"name": "Product Upload Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Upload product image
    image_data = b"fake product image content"
    image_file = BytesIO(image_data)
    image_file.name = "company_logo.png"

    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("company_logo.png", image_file, "image/png")}
    )
    assert response.status_code == 200
    product = response.json()
    assert "id" in product

    # Verify product is associated with project
    # This would typically be tested by checking project details endpoint
    # For now, just ensure upload succeeded

def test_multiple_product_uploads():
    """Test uploading multiple products to same project"""

    project_data = {"name": "Multiple Products Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Upload first product
    image_data1 = b"product 1 image"
    image_file1 = BytesIO(image_data1)
    image_file1.name = "product1.jpg"
    response1 = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("product1.jpg", image_file1, "image/jpeg")}
    )
    assert response1.status_code == 200

    # Upload second product
    image_data2 = b"product 2 image"
    image_file2 = BytesIO(image_data2)
    image_file2.name = "product2.jpg"
    response2 = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("product2.jpg", image_file2, "image/jpeg")}
    )
    assert response2.status_code == 200

    # Products should have different IDs
    product1 = response1.json()
    product2 = response2.json()
    assert product1["id"] != product2["id"]

def test_product_upload_file_types():
    """Test uploading different file types"""

    project_data = {"name": "File Types Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    test_files = [
        ("logo.png", b"png content", "image/png"),
        ("logo.jpg", b"jpg content", "image/jpeg"),
        ("logo.webp", b"webp content", "image/webp"),
        ("logo.svg", b"<svg></svg>", "image/svg+xml")
    ]

    for filename, content, mimetype in test_files:
        image_file = BytesIO(content)
        image_file.name = filename

        response = client.post(
            f"/projects/{project_id}/product",
            files={"image": (filename, image_file, mimetype)}
        )
        # Should either succeed or fail based on supported types
        assert response.status_code in [200, 400, 422]

def test_product_upload_size_limits():
    """Test product upload with different file sizes"""

    project_data = {"name": "Size Limits Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Small file
    small_data = b"small"
    small_file = BytesIO(small_data)
    small_file.name = "small.jpg"
    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("small.jpg", small_file, "image/jpeg")}
    )
    assert response.status_code in [200, 400, 422]

    # Large file (simulate)
    large_data = b"x" * 1000000  # 1MB
    large_file = BytesIO(large_data)
    large_file.name = "large.jpg"
    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("large.jpg", large_file, "image/jpeg")}
    )
    # Should either succeed or fail based on size limits
    assert response.status_code in [200, 400, 413, 422]

def test_product_upload_security():
    """Test security aspects of product upload"""

    project_data = {"name": "Security Test"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Try uploading executable file
    exe_data = b"fake exe content"
    exe_file = BytesIO(exe_data)
    exe_file.name = "malware.exe"
    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("malware.exe", exe_file, "application/octet-stream")}
    )
    # Should reject non-image files
    assert response.status_code in [400, 422]

    # Try with malicious filename
    malicious_data = b"image content"
    malicious_file = BytesIO(malicious_data)
    malicious_file.name = "../../../etc/passwd"
    response = client.post(
        f"/projects/{project_id}/product",
        files={"image": ("../../../etc/passwd", malicious_file, "image/jpeg")}
    )
    # Should sanitize filename
    assert response.status_code in [200, 400, 422]
