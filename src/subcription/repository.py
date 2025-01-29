from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.constants import DB_NAMING_CONVENTION
from src.subcription.exception import SubcriptionNotFound
from src.subcription.models import Subcription


class SubcriptionRepository:
    async def get_subcription(self, subcription_id: str) -> Subcription:
        session = await get_db_session()

        val = await session.execute(
            select(SubscriptionDB).where(SubscriptionDB.id == subcription_id)
        )

        subcription = val.scalar()
        if subcription is None:
            raise SubcriptionNotFound

        return Subcription(
            id=subcription.id,
            title=subcription.title,
            is_active=subcription.is_active,
            cost=subcription.cost,
            duration=subcription.duration,
            photo_by_image_limit=subcription.photo_by_image_limit,
            photo_by_prompt_limit=subcription.photo_by_prompt_limit,
            started_at=subcription.started_at,
            ended_at=subcription.ended_at,
        )


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    pass


class SubscriptionDB(Base):
    __tablename__ = "subcriptions"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]

    is_active: Mapped[bool]

    cost: Mapped[int]
    duration: Mapped[int]
    photo_by_prompt_limit: Mapped[int]
    photo_by_image_limit: Mapped[int]

    started_at: Mapped[datetime]
    ended_at: Mapped[Optional[datetime]]
