from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, func, select
from sqlalchemy.orm import Mapped, mapped_column

from src.database import get_db_session
from src.user.exception import UserNotFound
from src.user.model import User, UserSubscriptionState, UserType

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from src.constants import DB_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    pass


class UserRepository:
    async def save_user(self, user: User) -> str:
        session = await get_db_session()

        user_db = UserDB(
            id=user.user_id,
            nickname=user.nickname,
            tg_premium=user.tg_premium,
            user_type=user.user_type,
            )

        session.add(user_db)

        await session.commit()

        return user_db.id

    async def get_user(self, user_id: str) -> User:
        session = await get_db_session()

        res = await session.execute(
                select(UserDB).where(UserDB.id == user_id)
                )

        user = res.scalar()
        if user is None:
            raise UserNotFound

        return user.to_model()

    async def get_user_subcription_state(self, user: User) -> UserSubscriptionState:
        session = await get_db_session()

        subcription = await session.execute(
            select(UserSubscriptionStateDB).
            where(UserSubscriptionStateDB.user_id == user.user_id),
        )

        sub = subcription.scalar()

        if sub is None:
            raise UserNotFound

        return sub.to_model()


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(1000))
    tg_premium: Mapped[bool]
    user_type: Mapped[UserType]
    models_max: Mapped[int]

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_model(self) -> User:
        return User(
                user_id=self.id,
                nickname=self.nickname,
                user_type=self.user_type,
                tg_premium=self.tg_premium,
                started_at=self.started_at,
                models_max=self.models_max,
                )


class UserSubscriptionStateDB(Base):
    __tablename__ = 'user_subcription'

    user_id: Mapped[str] = mapped_column(primary_key=True)
    subcription_id: Mapped[str] = mapped_column()

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_date: Mapped[datetime] = mapped_column()

    photo_by_promnt_count: Mapped[int] = mapped_column()
    photo_by_image_count: Mapped[int] = mapped_column()

    def to_model(self) -> UserSubscriptionState:
        return UserSubscriptionState(
            user_id=self.user_id,
            subcription_id=self.subcription_id,
            start_date=self.start_date,
            end_date=self.end_date,
            photo_by_image_count=self.photo_by_image_count,
            photo_by_promnt_count=self.photo_by_promnt_count,
        )

