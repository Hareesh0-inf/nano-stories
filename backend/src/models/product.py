from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)  # URL to uploaded image file
    filename: Mapped[str] = mapped_column(String, nullable=True)
    content_type: Mapped[str] = mapped_column(String, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="products")

    def __repr__(self):
        return f"<Product(id='{self.id}', project_id='{self.project_id}', name='{self.name}', filename='{self.filename}')>"
