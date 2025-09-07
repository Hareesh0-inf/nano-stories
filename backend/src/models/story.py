from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import BaseModel

class Story(BaseModel):
    __tablename__ = "stories"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    story_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationship
    project = relationship("Project", back_populates="stories")

    def __repr__(self):
        return f"<Story(id='{self.id}', project_id='{self.project_id}')>"
