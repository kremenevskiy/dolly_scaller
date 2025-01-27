from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Subcription(BaseModel):
    id: str
    title: str

    is_active: bool

    cost: int
    duration: int
    photo_by_prompt_limit: int
    photo_by_image_limit: int

    started_at: datetime
    ended_at: Optional[datetime] = None
