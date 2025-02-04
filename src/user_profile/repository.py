from src.database import DatabaseManager
from src.user_profile import model


class UserProfileRepository:
    @staticmethod
    async def get_photo_formats() -> list[model.PhotoFormat]:
        query = """
            SELECT id, format, height, width
            FROM formats
        """
        rows = await DatabaseManager.fetch(query)
        return [model.PhotoFormat.from_row(row) for row in rows]

    @staticmethod
    async def get_user_photo_format(user_id: str) -> list[model.PhotoFormat]:
        query = """
            SELECT f.id, f.format, f.height, f.width
            FROM user_profiles up
            JOIN formats f ON up.format_id = f.id
            WHERE up.user_id = $1';
        """
        row = await DatabaseManager.fetchrow(query, user_id)

        return model.PhotoFormat.from_row(row)

    @staticmethod
    async def check_user_format_exists(user_id: str) -> list[model.PhotoFormat]:
        query = """
            SELECT EXISTS (
                SELECT 1 FROM user_profiles WHERE user_id = $1
            );
        """
        return await DatabaseManager.fetchval(query, user_id)

    @staticmethod
    async def change_user_photo_format(user_id: str, format_id: int) -> None:
        query = """
            INSERT INTO user_profiles (user_id, format_id)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE
            SET format_id = EXCLUDED.format_id
        """

        await DatabaseManager.execute(query, user_id, format_id)

    # @staticmethod
    # async def get_subscription(subscription_id: int) -> model.Subscription:
    #     query = """
    #         SELECT id, subscription_name, subscription_type, cost_rubles, cost_stars,
    #             duration, start_date, end_date,
    #             models_count, photos_by_prompt_count, photos_by_image_count
    #         FROM subscriptions_details
    #         WHERE id = $1;
    #     """
    #     row = await DatabaseManager.fetchrow(query, subscription_id)
    #     return model.Subscription.from_row(row) if row else None
