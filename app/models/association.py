from sqlalchemy import Table, Column, ForeignKey
from .base import Base

tag_image_association_table = Table(
    "service_relation_tag_image",
    Base.metadata,
    Column(
        "image_id",
        ForeignKey("service_images.id"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("service_tags.id"),
        primary_key=True,
    ),
)
