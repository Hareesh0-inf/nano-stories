from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import BaseModel

class Background(BaseModel):
    __tablename__ = "backgrounds"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    scene_details: Mapped[str] = mapped_column(Text, nullable=False)
    lighting: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)  # Generated image URL

    # Relationship
    project = relationship("Project", back_populates="backgrounds")

    def __repr__(self):
        return f"<Background(id='{self.id}', project_id='{self.project_id}')>"
