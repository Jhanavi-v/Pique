from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    color_hex = Column(String, nullable=False)
    size = Column(String, nullable=False)
    fit = Column(String, nullable=False)
    rating = Column(Integer, default=3)
    wash_status = Column(String, default="clean")
    wear_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())