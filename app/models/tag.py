from .association import tag_image_association_table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from .base import Base


class Tag(Base):
    __tablename__ = "service_tags"

    type: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
    meta: Mapped[list] = mapped_column(JSONB, default={})
    note: Mapped[str] = mapped_column(nullable=True)
    images_count: Mapped[int]

    images: Mapped[list["Image"]] = relationship(
        secondary=tag_image_association_table,
        back_populates="tags",
    )
