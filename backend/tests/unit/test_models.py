"""
Unit tests for database models
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models and database setup
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from models.base import Base
from models.project import Project
from models.character import Character
from models.product import Product
from models.background import Background
from models.story import Story
from models.image import Image

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL)
    
    # Drop all tables first to ensure clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

class TestProjectModel:
    """Test cases for Project model"""

    def test_project_creation(self, test_db):
        """Test creating a new project"""
        project = Project(name="Test Brand Story")
        test_db.add(project)
        test_db.commit()
        test_db.refresh(project)

        assert project.id is not None
        assert project.name == "Test Brand Story"
        assert project.created_at is not None
        assert project.updated_at is not None

    def test_project_str_representation(self, test_db):
        """Test string representation of project"""
        project = Project(name="Test Project")
        assert str(project) == "<Project(id=None, name='Test Project')>"

    def test_project_with_id_str_representation(self, test_db):
        """Test string representation with ID"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()
        test_db.refresh(project)

        assert f"id={project.id}" in str(project)
        assert "name='Test Project'" in str(project)

class TestCharacterModel:
    """Test cases for Character model"""

    def test_character_creation(self, test_db):
        """Test creating a new character"""
        # First create a project
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        character = Character(
            project_id=project.id,
            details="A professional business person",
            personality="confident",
            image_url="https://example.com/character.jpg"
        )
        test_db.add(character)
        test_db.commit()
        test_db.refresh(character)

        assert character.id is not None
        assert character.project_id == project.id
        assert character.details == "A professional business person"
        assert character.personality == "confident"
        assert character.image_url == "https://example.com/character.jpg"
        assert character.created_at is not None

    def test_character_relationship(self, test_db):
        """Test character-project relationship"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        character = Character(
            project_id=project.id,
            details="Test character",
            personality="Friendly and creative",
            image_url="https://example.com/test.jpg"
        )
        test_db.add(character)
        test_db.commit()

        # Test relationship from character to project
        assert character.project.id == project.id
        assert character.project.name == "Test Project"

        # Test relationship from project to character
        assert len(project.characters) == 1
        assert project.characters[0].id == character.id

class TestProductModel:
    """Test cases for Product model"""

    def test_product_creation(self, test_db):
        """Test creating a new product"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        product = Product(
            project_id=project.id,
            filename="test_product.jpg",
            content_type="image/jpeg",
            image_url="https://example.com/product.jpg"
        )
        test_db.add(product)
        test_db.commit()
        test_db.refresh(product)

        assert product.id is not None
        assert product.project_id == project.id
        assert product.filename == "test_product.jpg"
        assert product.content_type == "image/jpeg"
        assert product.image_url == "https://example.com/product.jpg"

    def test_product_relationship(self, test_db):
        """Test product-project relationship"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        product = Product(
            project_id=project.id,
            filename="test_product.jpg",
            image_url="https://example.com/test.jpg"
        )
        test_db.add(product)
        test_db.commit()

        # Test relationships
        assert product.project.id == project.id
        assert len(project.products) == 1
        assert project.products[0].id == product.id

class TestBackgroundModel:
    """Test cases for Background model"""

    def test_background_creation(self, test_db):
        """Test creating a new background"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        background = Background(
            project_id=project.id,
            scene_details="Modern office setting",
            lighting="natural daylight",
            image_url="https://example.com/background.jpg"
        )
        test_db.add(background)
        test_db.commit()
        test_db.refresh(background)

        assert background.id is not None
        assert background.project_id == project.id
        assert background.scene_details == "Modern office setting"
        assert background.lighting == "natural daylight"
        assert background.image_url == "https://example.com/background.jpg"

    def test_background_relationship(self, test_db):
        """Test background-project relationship"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        background = Background(
            project_id=project.id,
            scene_details="Test scene",
            lighting="natural daylight",
            image_url="https://example.com/test.jpg"
        )
        test_db.add(background)
        test_db.commit()

        # Test relationships
        assert background.project.id == project.id
        assert len(project.backgrounds) == 1
        assert project.backgrounds[0].id == background.id

class TestStoryModel:
    """Test cases for Story model"""

    def test_story_creation(self, test_db):
        """Test creating a new story"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        story_text = "This is a compelling brand story about our amazing product."
        story = Story(
            project_id=project.id,
            story_text=story_text
        )
        test_db.add(story)
        test_db.commit()
        test_db.refresh(story)

        assert story.id is not None
        assert story.project_id == project.id
        assert story.story_text == story_text

    def test_story_relationship(self, test_db):
        """Test story-project relationship"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        story = Story(
            project_id=project.id,
            story_text="Test story"
        )
        test_db.add(story)
        test_db.commit()

        # Test relationships
        assert story.project.id == project.id
        assert len(project.stories) == 1
        assert project.stories[0].id == story.id

class TestImageModel:
    """Test cases for Image model"""

    def test_image_creation(self, test_db):
        """Test creating a new image"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        image = Image(
            project_id=project.id,
            image_url="https://example.com/generated.jpg",
            prompt="A beautiful brand story image",
            image_type="final",
            fusion_style="professional"
        )
        test_db.add(image)
        test_db.commit()
        test_db.refresh(image)

        assert image.id is not None
        assert image.project_id == project.id
        assert image.image_url == "https://example.com/generated.jpg"
        assert image.prompt == "A beautiful brand story image"
        assert image.fusion_style == "professional"

    def test_image_relationship(self, test_db):
        """Test image-project relationship"""
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        image = Image(
            project_id=project.id,
            image_url="https://example.com/test.jpg",
            prompt="Test prompt",
            image_type="character"
        )
        test_db.add(image)
        test_db.commit()

        # Test relationships
        assert image.project.id == project.id
        assert len(project.images) == 1
        assert project.images[0].id == image.id

class TestModelRelationships:
    """Test cases for complex model relationships"""

    def test_complete_project_relationships(self, test_db):
        """Test all relationships for a complete project"""
        # Create project
        project = Project(name="Complete Brand Story Project")
        test_db.add(project)
        test_db.commit()

        # Create character
        character = Character(
            project_id=project.id,
            details="Professional character",
            personality="Confident and innovative",
            image_url="https://example.com/char.jpg"
        )
        test_db.add(character)

        # Create product
        product = Product(
            project_id=project.id,
            filename="amazing_product.jpg",
            image_url="https://example.com/prod.jpg"
        )
        test_db.add(product)

        # Create background
        background = Background(
            project_id=project.id,
            scene_details="Modern setting",
            lighting="bright studio lighting",
            image_url="https://example.com/bg.jpg"
        )
        test_db.add(background)

        # Create story
        story = Story(
            project_id=project.id,
            story_text="Amazing brand story"
        )
        test_db.add(story)

        # Create images
        image1 = Image(
            project_id=project.id,
            image_url="https://example.com/img1.jpg",
            prompt="First generated image",
            image_type="character"
        )
        image2 = Image(
            project_id=project.id,
            image_url="https://example.com/img2.jpg",
            prompt="Second generated image",
            image_type="background"
        )
        test_db.add_all([image1, image2])
        test_db.commit()

        # Verify all relationships
        assert len(project.characters) == 1
        assert len(project.products) == 1
        assert len(project.backgrounds) == 1
        assert len(project.stories) == 1
        assert len(project.images) == 2

        # Verify reverse relationships
        assert character.project.id == project.id
        assert product.project.id == project.id
        assert background.project.id == project.id
        assert story.project.id == project.id
        assert image1.project.id == project.id
        assert image2.project.id == project.id

    def test_cascade_delete(self, test_db):
        """Test that related records are properly handled on delete"""
        # Create project with relationships
        project = Project(name="Test Project")
        test_db.add(project)
        test_db.commit()

        character = Character(
            project_id=project.id,
            details="Test character",
            personality="Friendly character",
            image_url="https://example.com/test.jpg"
        )
        test_db.add(character)
        test_db.commit()

        # Verify character exists
        assert test_db.query(Character).filter(Character.project_id == project.id).first() is not None

        # Delete project (this should cascade delete character due to foreign key constraint)
        test_db.delete(project)
        test_db.commit()

        # Verify character is gone (cascade delete)
        assert test_db.query(Character).filter(Character.project_id == project.id).first() is None
