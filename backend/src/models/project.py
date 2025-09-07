from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="project", cascade="all, delete-orphan")
    backgrounds = relationship("Background", back_populates="project", cascade="all, delete-orphan")
    stories = relationship("Story", back_populates="project", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
