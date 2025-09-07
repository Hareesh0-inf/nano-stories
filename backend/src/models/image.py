from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import BaseModel

class Image(BaseModel):
    __tablename__ = "images"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)  # Generated prompt used
    image_url: Mapped[str] = mapped_column(String, nullable=False)  # Generated image URL
    image_type: Mapped[str] = mapped_column(String, nullable=False)  # Type: 'character', 'background', 'final'
    fusion_style: Mapped[str] = mapped_column(String, nullable=True)  # For final images: fusion style used

    # Relationship
    project = relationship("Project", back_populates="images")

    def __repr__(self):
        return f"<Image(id='{self.id}', project_id='{self.project_id}', type='{self.image_type}')>"
