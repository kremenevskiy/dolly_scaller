from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import get_db_session
from src.user.model import User, UserType

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from src.constants import DB_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    pass


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(1000))
    tg_premium: Mapped[Optional[bool]]
    user_type: Mapped[UserType]

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


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
