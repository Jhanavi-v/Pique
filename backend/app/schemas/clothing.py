from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClothingCreate(BaseModel):
    name: str
    category: str
    color_hex: str
    size: str
    fit: str
    rating: Optional[int] = 3
    wash_status: Optional[str] = "clean"


class ClothingResponse(BaseModel):
    id: int
    name: str
    category: str
    color_hex: str
    size: str
    fit: str
    rating: int
    wash_status: str
    wear_count: int
    created_at: datetime

    class Config:
        from_attributes = True