from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import Depends

# Import models and services
from ..models.product import Product
from ..services.gemini_service import GeminiService
from ..database import get_db, save_product, get_project

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: str
    image_url: str

@router.post("/projects/{project_id}/product/generate", response_model=ProductResponse)
async def generate_product(project_id: str, product: ProductCreate, db: Session = Depends(get_db)):
    """
    Generate a product image for the project using AI
    """
    if not product.name.strip():
        raise HTTPException(status_code=422, detail="Product name cannot be empty")

    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Initialize Gemini service
        gemini_service = GeminiService()

        # Generate product image
        description = product.description or "high-quality product"
        image_url = gemini_service.generate_product_image(
            name=product.name,
            description=description
        )

        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to generate product image")

        # Save product to database
        db_product = save_product(
            db=db,
            project_id=project_id,
            name=product.name,
            description=description,
            image_url=image_url
        )

        return ProductResponse(
            id=str(db_product.id),  # Convert to string for API response
            image_url=image_url
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating product: {str(e)}")

@router.post("/projects/{project_id}/product/upload", response_model=ProductResponse)
async def upload_product(project_id: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a product image for the project
    """
    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await image.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")

    try:
        # Generate product ID
        product_id = str(uuid.uuid4())

        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads/products")
        uploads_dir.mkdir(parents=True, exist_ok=True)

        # Save file with product ID as filename
        file_extension = Path(image.filename).suffix or ".png"
        filename = f"{product_id}{file_extension}"
        file_path = uploads_dir / filename

        with open(file_path, "wb") as f:
            f.write(file_content)

        # Create image URL for local file
        image_url = f"/uploads/products/{filename}"

        # Save product to database
        db_product = save_product(
            db=db,
            project_id=project_id,
            name=image.filename,
            description="Uploaded product image",
            image_url=image_url
        )

        return ProductResponse(
            id=str(db_product.id),  # Convert to string for API response
            image_url=image_url
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading product: {str(e)}")
