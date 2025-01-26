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

    started_at: Optional[datetime] = None


class UserResponse(BaseModel):
    user_id: str
