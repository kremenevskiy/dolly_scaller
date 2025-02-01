from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Gender(Enum):
    MALE = 'man'
    FEMALE = 'woman'


class ModelStatus(Enum):
    WAITING_FOR_TRAINING = 'waiting_for_training'
    TRAIN_STARTED = 'train_started'
    READY = 'ready'


class Model(BaseModel):
    id: Optional[int] = None
    name: str
    user_id: str

    gender: Gender
    link_to_adls: Optional[str] = None
    status: ModelStatus
    photo_info: Optional[dict] = None
