from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import BaseModel

class Character(BaseModel):
    __tablename__ = "characters"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    personality: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)  # Generated image URL

    # Relationship
    project = relationship("Project", back_populates="characters")

    def __repr__(self):
        return f"<Character(id='{self.id}', project_id='{self.project_id}')>"
