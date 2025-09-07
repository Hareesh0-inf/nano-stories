from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import uuid
from sqlalchemy.orm import Session

# Import models and database
from ..models.project import Project
from ..database import get_db, save_project

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: str

@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project
    """
    if not project.name.strip():
        raise HTTPException(status_code=422, detail="Project name cannot be empty")

    try:
        # Generate UUID for project ID
        project_id = str(uuid.uuid4())

        # Save to database
        db_project = save_project(db, project.name)

        return ProjectResponse(
            id=str(db_project.id),  # Convert to string for API response
            name=db_project.name,
            created_at=db_project.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")
