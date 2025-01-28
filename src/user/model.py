from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserType(str, Enum):
    CUSTOMER = "customer"
    VIP = "vip"
    WHITELISTED = "whitelisted"


class User(BaseModel):
    user_id: str = Field(min_length=1, max_length=1000)
    nickname: str
    user_type: UserType
    tg_premium: bool
    models_max: int

    started_at: Optional[datetime] = None


class UserResponse(BaseModel):
    user_id: str


class UserSubscriptionState(BaseModel):
    user_id: str
    subcription_id: str

    start_date: datetime
    end_date: datetime

    photo_by_promnt_count: int
    photo_by_image_count: int


class OperationType(Enum):
    GENERATE_BY_IMAGE = "generate_by_image"
    GENERATE_BY_PROMNT = "generate_by_prompt"
    CREATE_MODEL = "create_model"
