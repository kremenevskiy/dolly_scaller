
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, func, select


from src.constants import DB_NAMING_CONVENTION
from src.database import get_db_session
from src.model.models import Gender, Model, ModelStatus


class ModelRepository:
    async def get_user_model_count(self, user_id: str) -> int:

        session = await get_db_session()

        val = await session.execute(
            select(func.count(ModelDB.user_id)).
            group_by(ModelDB.user_id).where(ModelDB.user_id == user_id)
            )

        count = val.scalar()
        if count is None:
            return 0

        return int(count)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    pass


class ModelDB(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    name: Mapped[str]
    user_id: Mapped[str]

    gender: Mapped[Gender]
    link_to_adls: Mapped[Optional[str]]
    status: Mapped[ModelStatus]
    photo_info: Mapped[Optional[str]]

    def to_model(self) -> Model:
        return Model(
                id=self.id,
                name=self.name,
                user_id=self.user_id,
                gender=self.gender,
                link_to_adls=self.link_to_adls,
                status=self.status,
                photo_info=self.photo_info,
                )
