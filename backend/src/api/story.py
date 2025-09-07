from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from sqlalchemy.orm import Session
from fastapi import Depends

# Import models
from ..models.story import Story
from ..database import get_db, save_story, get_project

router = APIRouter()

class StoryCreate(BaseModel):
    story_text: str

class StoryResponse(BaseModel):
    id: str

@router.post("/projects/{project_id}/story", response_model=StoryResponse)
async def create_story(project_id: str, story: StoryCreate, db: Session = Depends(get_db)):
    """
    Set the story text for the project
    """
    if not story.story_text.strip():
        raise HTTPException(status_code=422, detail="Story text cannot be empty")

    # Check if project exists
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # Save story to database
        db_story = save_story(
            db=db,
            project_id=project_id,
            story_text=story.story_text
        )

        return StoryResponse(id=str(db_story.id))  # Convert to string for API response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving story: {str(e)}")
