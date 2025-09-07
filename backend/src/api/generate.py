from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import base64
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import Depends

# Import models and services
from ..models.image import Image
from ..models.character import Character
from ..models.product import Product
from ..models.background import Background
from ..models.story import Story
from ..services.gemini_service import GeminiService
from ..database import get_db, save_image, get_project

router = APIRouter()

class GeneratedImage(BaseModel):
    id: str
    prompt: str
    image_url: str
    fusion_style: Optional[str] = None

class GenerateResponse(BaseModel):
    images: List[GeneratedImage]

@router.post("/projects/{project_id}/generate", response_model=GenerateResponse)
async def generate_images(project_id: str, db: Session = Depends(get_db)):
    """
    Generate final fused images combining character, product, background, and story
    """
    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Retrieve project components from database
        character = db.query(Character).filter(Character.project_id == project_id).first()
        product = db.query(Product).filter(Product.project_id == project_id).first()
        background = db.query(Background).filter(Background.project_id == project_id).first()
        story = db.query(Story).filter(Story.project_id == project_id).first()

        # Check if all required components exist
        if not all([character, product, background, story]):
            missing_components = []
            if not character: missing_components.append("character")
            if not product: missing_components.append("product")
            if not background: missing_components.append("background")
            if not story: missing_components.append("story")

            raise HTTPException(
                status_code=400,
                detail=f"Missing required components: {', '.join(missing_components)}. Please ensure all components are created first."
            )

        # Prepare image data for fusion
        character_image_data = None
        product_image_data = None
        background_image_data = None

        # Handle character image
        if character.image_url.startswith('data:'):
            # Base64 encoded image
            header, encoded = character.image_url.split(',', 1)
            character_image_data = base64.b64decode(encoded)
        elif character.image_url.startswith('/mock-images/') or character.image_url.startswith('generated_') or character.image_url.startswith('/uploads/'):
            # Mock or static file URL - read from the actual file path or use placeholder data
            if character.image_url.startswith('/uploads/'):
                actual_path = character.image_url.replace('/uploads/', 'uploads/')
                try:
                    with open(actual_path, "rb") as f:
                        character_image_data = f.read()
                    print(f"ℹ️  Read character image from file: {character.image_url}")
                except FileNotFoundError:
                    # If file doesn't exist, use placeholder data
                    character_image_data = b"mock_character_image_data"
                    print(f"ℹ️  Using mock character image data for: {character.image_url}")
            else:
                # Mock image - create placeholder data
                character_image_data = b"mock_character_image_data"
                print(f"ℹ️  Using mock character image data for: {character.image_url}")
        else:
            # File path
            try:
                with open(character.image_url, "rb") as f:
                    character_image_data = f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Character image file not found")

        # Handle product image
        if product.image_url.startswith('data:'):
            # Base64 encoded image
            header, encoded = product.image_url.split(',', 1)
            product_image_data = base64.b64decode(encoded)
        elif product.image_url.startswith('/mock-images/') or product.image_url.startswith('generated_') or product.image_url.startswith('/uploads/'):
            # Mock or static file URL - read from the actual file path or use placeholder data
            if product.image_url.startswith('/uploads/'):
                actual_path = product.image_url.replace('/uploads/', 'uploads/')
                try:
                    with open(actual_path, "rb") as f:
                        product_image_data = f.read()
                    print(f"ℹ️  Read product image from file: {product.image_url}")
                except FileNotFoundError:
                    # If file doesn't exist, use placeholder data
                    product_image_data = b"mock_product_image_data"
                    print(f"ℹ️  Using mock product image data for: {product.image_url}")
            else:
                # Mock image - create placeholder data
                product_image_data = b"mock_product_image_data"
                print(f"ℹ️  Using mock product image data for: {product.image_url}")
        else:
            # File path
            try:
                with open(product.image_url, "rb") as f:
                    product_image_data = f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Product image file not found")

        # Handle background image
        if background.image_url.startswith('data:'):
            # Base64 encoded image
            header, encoded = background.image_url.split(',', 1)
            background_image_data = base64.b64decode(encoded)
        elif background.image_url.startswith('/mock-images/') or background.image_url.startswith('generated_') or background.image_url.startswith('/uploads/'):
            # Mock or static file URL - read from the actual file path or use placeholder data
            if background.image_url.startswith('/uploads/'):
                actual_path = background.image_url.replace('/uploads/', 'uploads/')
                try:
                    with open(actual_path, "rb") as f:
                        background_image_data = f.read()
                    print(f"ℹ️  Read background image from file: {background.image_url}")
                except FileNotFoundError:
                    # If file doesn't exist, use placeholder data
                    background_image_data = b"mock_background_image_data"
                    print(f"ℹ️  Using mock background image data for: {background.image_url}")
            else:
                # Mock image - create placeholder data
                background_image_data = b"mock_background_image_data"
                print(f"ℹ️  Using mock background image data for: {background.image_url}")
        else:
            # File path
            try:
                with open(background.image_url, "rb") as f:
                    background_image_data = f.read()
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Background image file not found")

        # Initialize Gemini service
        gemini_service = GeminiService()

        # Generate fused images
        fused_images = gemini_service.generate_final_images(
            character_image_data=character_image_data,
            product_image_data=product_image_data,
            background_image_data=background_image_data,
            story=story.story_text
        )

        if not fused_images:
            raise HTTPException(status_code=500, detail="Failed to generate fused images")

        # Convert to response format and save to database
        images = []
        for img in fused_images:
            image_id = str(uuid.uuid4())
            image_url = img.get("image_url", "")
            prompt = img.get("prompt", "")
            fusion_style = img.get("fusion_style")

            # Save generated image to database
            db_image = save_image(
                db=db,
                project_id=project_id,
                prompt=prompt,
                image_url=image_url,
                image_type="final",
                fusion_style=fusion_style
            )

            images.append(GeneratedImage(
                id=str(db_image.id),  # Convert to string for API response
                prompt=prompt,
                image_url=image_url,
                fusion_style=fusion_style
            ))

        return GenerateResponse(images=images)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating images: {str(e)}")
