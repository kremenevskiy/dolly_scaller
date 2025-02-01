from enum import Enum

from pydantic import BaseModel


class Gender(Enum):
    MALE = 'man'
    FEMALE = 'woman'


class ModelStatus(Enum):
    WAITING_FOR_TRAINING = 'waiting_for_training'
    TRAIN_STARTED = 'train_started'
    READY = 'ready'


class Model(BaseModel):
    id: int | None = None
    name: str
    user_id: str

    gender: Gender
    link_to_adls: str | None = None
    status: ModelStatus
    photo_info: dict | None = None
