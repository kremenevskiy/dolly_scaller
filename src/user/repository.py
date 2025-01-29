from typing import Optional

from src.database import DatabaseManager
from src.user.exception import UserNotFound
from src.user.model import User, UserSubscriptionState, UserType


class UserRepository:
    @staticmethod
    async def create_new_user(user: User) -> None:
        query = """
            INSERT INTO users (user_id, username, user_first_name, user_last_name,
                                tg_premium, user_type, models_created, models_max)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (user_id) DO UPDATE
            SET username = EXCLUDED.username,
                user_first_name = EXCLUDED.user_first_name,
                user_last_name = EXCLUDED.user_last_name,
                tg_premium = EXCLUDED.tg_premium,
                user_type = EXCLUDED.user_type,
                models_created = EXCLUDED.models_created,
                models_max = EXCLUDED.models_max
        """

        await DatabaseManager.execute(
            query,
            user.user_id,
            user.username,
            user.user_first_name,
            user.user_last_name,
            user.tg_premium,
            user.user_type.value,
            user.models_created,
            user.models_max,
        )

    @staticmethod
    async def get_user_id_from_user_username(username: str) -> Optional[str]:
        query = """
            SELECT user_id
            FROM users
            WHERE username = $1
        """
        return await DatabaseManager.fetchval(query, username)

    # async def get_user(self, user_id: str) -> User:
    #     session = await get_db_session()

    #     res = await session.execute(select(UserDB).where(UserDB.id == user_id))

    #     user = res.scalar()
    #     if user is None:
    #         raise UserNotFound

    #     return user.to_model()

    # async def get_user_subcription_state(self, user_id: str) -> UserSubscriptionState:
    #     session = await get_db_session()

    #     subcription = await session.execute(
    #         select(UserSubscriptionStateDB).where(
    #             UserSubscriptionStateDB.user_id == user_id
    #         ),
    #     )

    #     sub = subcription.scalar()

    #     if sub is None:
    #         raise UserNotFound

    #     return sub.to_model()

    # async def save_user_sub_state(self, state: UserSubscriptionState):
    #     session = await get_db_session()

    #     stateDB = UserSubscriptionStateDB().from_model(state)

    #     await session.merge(stateDB)
    #     await session.commit()


# class UserSubscriptionStateDB(Base):
#     __tablename__ = "user_subcription"

#     user_id: Mapped[str] = mapped_column(primary_key=True)
#     subcription_id: Mapped[str] = mapped_column()

#     start_date: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

#     photo_by_promnt_count: Mapped[int] = mapped_column()
#     photo_by_image_count: Mapped[int] = mapped_column()

#     def to_model(self) -> UserSubscriptionState:
#         return UserSubscriptionState(
#             user_id=self.user_id,
#             subcription_id=self.subcription_id,
#             start_date=self.start_date,
#             end_date=self.end_date,
#             photo_by_image_count=self.photo_by_image_count,
#             photo_by_promnt_count=self.photo_by_promnt_count,
#         )

#     def from_model(self, model: UserSubscriptionState):
#         self.user_id = model.user_id
#         self.subcription_id = model.subcription_id
#         self.start_date = model.start_date
#         self.end_date = model.end_date

#         self.photo_by_promnt_count = model.photo_by_promnt_count
#         self.photo_by_image_count = model.photo_by_image_count

#         return self
