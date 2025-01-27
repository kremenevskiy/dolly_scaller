

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


class ModelStatus:
    TRAIN_STARTED = "train_started"
    READY = 'ready'


class Model(BaseModel):
    id: int
    name: str
    user_id: str

    gender: Gender
    link_to_adls: Optional[str]
    status: ModelStatus
    photo_info: Optional[str]
