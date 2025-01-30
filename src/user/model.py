import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class UserType(str, Enum):
    CUSTOMER = 'customer'
    VIP = 'vip'
    WHITELISTED = 'whitelisted'


class User(BaseModel):
    user_id: str

    username: str | None
    user_first_name: str | None
    user_last_name: str | None
    tg_premium: bool

    user_type: UserType

    models_max: int = 0

    date_joined: datetime.datetime | None = None

    @classmethod
    def from_row(cls, row):
        return cls(
            user_id=row['user_id'],
            username=row.get('username'),
            user_first_name=row.get('user_first_name'),
            user_last_name=row.get('user_last_name'),
            tg_premium=row['tg_premium'],
            user_type=UserType(row['user_type']),
            models_max=row.get('models_max', 0),
            date_joined=row.get('date_joined'),
        )


class SubcriptionStatus(Enum):
    ACTIVE = 'active'
    PENDING = 'pending'
    FINISHED = 'finished'


class UserSubscription(BaseModel):
    id: Optional[int] = None
    user_id: str
    subscription_id: int

    start_date: datetime.datetime
    end_date: datetime.datetime
    status: SubcriptionStatus

    photos_by_prompt_left: int
    photos_by_image_left: int


# TODO: проверить что и в старах и в рублях проходит через эту схему
class PaymentDetails(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    subscription_expiration_date: str | None = None
    is_recurring: bool | None = None
    is_first_recurring: bool | None = None
    shipping_option_id: str | None = None
    order_info: str | None = None


class UserSubscriptionRequest(BaseModel):
    user_id: str
    subscription_id: int


class UserSubscriptionPaymentRequest(BaseModel):
    user_id: str
    payment_details: PaymentDetails


class OperationType(Enum):
    GENERATE_BY_IMAGE = 'generate_by_image'
    GENERATE_BY_PROMNT = 'generate_by_prompt'
    CREATE_MODEL = 'create_model'
