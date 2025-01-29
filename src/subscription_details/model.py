import datetime

from pydantic import BaseModel


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
    photos_by_prompt_count: int
    photos_by_image_count: int

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            subscription_name=row["subscription_name"],
            subscription_type=row["subscription_type"],
            cost_rubles=row["cost_rubles"],
            cost_stars=row["cost_stars"],
            duration=row["duration"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            models_count=row["models_count"],
            photos_by_prompt_count=row["photos_by_prompt_count"],
            photos_by_image_count=row["photos_by_image_count"],
        )
