from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from fastapi import Depends

# Import models and services
from ..models.character import Character
from ..services.gemini_service import GeminiService
from ..database import get_db, save_character, get_project

router = APIRouter()

class CharacterCreate(BaseModel):
    details: str
    personality: Optional[str] = None

class CharacterResponse(BaseModel):
    id: str
    image_url: str

@router.post("/projects/{project_id}/character", response_model=CharacterResponse)
async def create_character(project_id: str, character: CharacterCreate, db: Session = Depends(get_db)):
    """
    Generate a character image for the project
    """
    if not character.details.strip():
        raise HTTPException(status_code=422, detail="Character details cannot be empty")

    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Initialize Gemini service
        gemini_service = GeminiService()

        # Generate character image
        personality = character.personality or "professional and approachable"
        image_url = gemini_service.generate_character_image(
            details=character.details,
            personality=personality
        )

        if not image_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate character image. Please check your GOOGLE_API_KEY in the .env file."
            )

        # Save character to database
        db_character = save_character(
            db=db,
            project_id=project_id,
            details=character.details,
            personality=personality,
            image_url=image_url
        )

        return CharacterResponse(
            id=str(db_character.id),  # Convert to string for API response
            image_url=image_url
        )

    except ValueError as e:
        # Handle API key configuration errors
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating character: {str(e)}")
