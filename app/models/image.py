from .association import tag_image_association_table
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from datetime import datetime
from .base import Base


class Image(Base):
    __tablename__ = "service_images"

    uploaded_by: Mapped[str] = mapped_column(String(255), index=True)
    path: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    meta: Mapped[list] = mapped_column(JSONB, default={})
    source: Mapped[str] = mapped_column(nullable=True)
    created: Mapped[datetime]
    updated: Mapped[datetime]

    tags: Mapped[list["Tag"]] = relationship(
        secondary=tag_image_association_table,
        back_populates="images",
    )

    @hybrid_property
    def url(self):
        return "/uploads" + self.path
