import datetime
import enum

from pydantic import BaseModel


class SubscriptionType(enum.Enum):
    MONTHLY = 'monthly'
    MODELS = 'models'
    GENERATIONS = 'generations'
    REFERRAL_GENERATIONS = 'referral_generations'


class Subscription(BaseModel):
    id: int
    subscription_name: str
    subscription_type: str
    cost_rubles: int
    cost_stars: int
    duration: int | None
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    models_count: int
    generation_photos_count: int

    def is_monthly_sub(self) -> bool:
        return self.subscription_type == SubscriptionType.MONTHLY.value

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            subscription_name=row['subscription_name'],
            subscription_type=row['subscription_type'],
            cost_rubles=row['cost_rubles'],
            cost_stars=row['cost_stars'],
            duration=row['duration'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            models_count=row['models_count'],
            generation_photos_count=row['generation_photos_count'],
        )
