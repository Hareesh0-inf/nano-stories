from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from fastapi import Depends

# Import models and services
from ..models.background import Background
from ..services.gemini_service import GeminiService
from ..database import get_db, save_background, get_project

router = APIRouter()

class BackgroundCreate(BaseModel):
    scene_details: str
    lighting: Optional[str] = None

class BackgroundResponse(BaseModel):
    id: str
    image_url: str

@router.post("/projects/{project_id}/background", response_model=BackgroundResponse)
async def create_background(project_id: str, background: BackgroundCreate, db: Session = Depends(get_db)):
    """
    Generate a background image for the project
    """
    if not background.scene_details.strip():
        raise HTTPException(status_code=422, detail="Scene details cannot be empty")

    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Initialize Gemini service
        gemini_service = GeminiService()

        # Generate background image
        lighting = background.lighting or "natural daylight"
        image_url = gemini_service.generate_background_image(
            scene_details=background.scene_details,
            lighting=lighting
        )

        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to generate background image")

        # Save background to database
        db_background = save_background(
            db=db,
            project_id=project_id,
            scene_details=background.scene_details,
            lighting=lighting,
            image_url=image_url
        )

        return BackgroundResponse(
            id=str(db_background.id),  # Convert to string for API response
            image_url=image_url
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating background: {str(e)}")
