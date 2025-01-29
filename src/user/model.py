import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UserType(str, Enum):
    CUSTOMER = "customer"
    VIP = "vip"
    WHITELISTED = "whitelisted"


class User(BaseModel):
    user_id: str

    username: str
    user_first_name: str
    user_last_name: str
    tg_premium: bool

    user_type: UserType

    models_created: int
    models_max: int

    date_joined: datetime.datetime | None = None


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
