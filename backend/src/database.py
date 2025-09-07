"""
Database configuration and session management for Nano Stories
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from typing import Generator

from .models.project import Project
from .models.character import Character
from .models.product import Product
from .models.background import Background
from .models.story import Story
from .models.image import Image

load_dotenv()
# Database URL - use SQLite for development, can be changed for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nano_stories.db")

# Create engine with appropriate settings for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    poolclass=StaticPool if DATABASE_URL.startswith("sqlite") else None,
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """
    Create all database tables
    """
    from .models.base import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Initialize database and create tables
    """
    try:
        create_tables()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Database operations helper functions
def save_project(db: Session, name: str) -> Project:
    """Save a new project to database"""
    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project(db: Session, project_id: str) -> Project:
    """Get project by ID"""
    return db.query(Project).filter(Project.id == project_id).first()

def save_character(db: Session, project_id: str, details: str, personality: str = None, image_url: str = None) -> Character:
    """Save a character to database"""
    character = Character(
        project_id=project_id,
        details=details,
        personality=personality,
        image_url=image_url
    )
    db.add(character)
    db.commit()
    db.refresh(character)
    return character

def save_product(db: Session, project_id: str, name: str = None, description: str = None, image_url: str = None) -> Product:
    """Save a product to database"""
    product = Product(
        project_id=project_id,
        name=name,
        description=description,
        image_url=image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def save_background(db: Session, project_id: str, scene_details: str, lighting: str = None, image_url: str = None) -> Background:
    """Save a background to database"""
    background = Background(
        project_id=project_id,
        scene_details=scene_details,
        lighting=lighting,
        image_url=image_url
    )
    db.add(background)
    db.commit()
    db.refresh(background)
    return background

def save_story(db: Session, project_id: str, story_text: str) -> Story:
    """Save a story to database"""
    story = Story(
        project_id=project_id,
        story_text=story_text
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story

def save_image(db: Session, project_id: str, image_url: str, prompt: str, image_type: str, fusion_style: str = None) -> Image:
    """Save a generated image to database"""
    image = Image(
        project_id=project_id,
        image_url=image_url,
        prompt=prompt,
        image_type=image_type,
        fusion_style=fusion_style
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_project_components(db: Session, project_id: str) -> dict:
    """Get all components for a project"""
    project = get_project(db, project_id)
    if not project:
        return None

    character = db.query(Character).filter(Character.project_id == project_id).first()
    product = db.query(Product).filter(Product.project_id == project_id).first()
    background = db.query(Background).filter(Background.project_id == project_id).first()
    story = db.query(Story).filter(Story.project_id == project_id).first()
    images = db.query(Image).filter(Image.project_id == project_id).all()

    return {
        "project": project,
        "character": character,
        "product": product,
        "background": background,
        "story": story,
        "images": images
    }

def get_character_image_url(db: Session, project_id: str) -> str:
    """Get character image URL for a project"""
    character = db.query(Character).filter(Character.project_id == project_id).first()
    return character.image_url if character else None

def get_product_image_url(db: Session, project_id: str) -> str:
    """Get product image URL for a project"""
    product = db.query(Product).filter(Product.project_id == project_id).first()
    return product.image_url if product else None

def get_background_image_url(db: Session, project_id: str) -> str:
    """Get background image URL for a project"""
    background = db.query(Background).filter(Background.project_id == project_id).first()
    return background.image_url if background else None

def get_story_text(db: Session, project_id: str) -> str:
    """Get story text for a project"""
    story = db.query(Story).filter(Story.project_id == project_id).first()
    return story.story_text if story else None
