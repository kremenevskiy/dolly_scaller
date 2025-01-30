import json
from typing import Optional

from src.database import DatabaseManager
from src.user import model


class UserRepository:
    @staticmethod
    async def create_new_user(user: model.User) -> None:
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

    @staticmethod
    async def add_user_to_whitelist(user_id: str) -> None:
        query = """
            UPDATE users
            SET user_type = $1
            WHERE user_id = $2
        """
        await DatabaseManager.execute(query, model.UserType.WHITELISTED.value, user_id)

    @staticmethod
    async def save_user_subscription(user_subscription: model.UserSubscription) -> None:
        deactivate_query = """
            UPDATE user_subscriptions
            SET is_active = FALSE
            WHERE user_id = $1;
        """

        await DatabaseManager.execute(deactivate_query, user_subscription.user_id)

        # Step 2: Insert the new subscription as active
        insert_query = """
            INSERT INTO user_subscriptions (user_id, subscription_id, start_date, end_date,
                                            photos_by_prompt_left, photos_by_image_left, is_active)
            VALUES ($1, $2, $3, $4, $5, $6, TRUE);
        """

        await DatabaseManager.execute(
            insert_query,
            user_subscription.user_id,
            user_subscription.subscription_id,
            user_subscription.start_date,
            user_subscription.end_date,
            user_subscription.photos_by_prompt_left,
            user_subscription.photos_by_image_left,
        )

    @staticmethod
    async def add_generations_to_active_subscription(
        user_id: str, photos_by_prompt: int, photos_by_image: int
    ) -> None:
        query = """
            UPDATE user_subscriptions
            SET photos_by_prompt_left = photos_by_prompt_left + $1,
                photos_by_image_left = photos_by_image_left + $2
            WHERE user_id = $3 AND is_active = TRUE;
        """
        await DatabaseManager.execute(query, photos_by_prompt, photos_by_image, user_id)

    @staticmethod
    async def increase_user_models_limit(user_id: str, models_count: int) -> None:
        query = """
            UPDATE users
            SET models_max = COALESCE(models_max, 0) + $1
            WHERE user_id = $2;
        """
        await DatabaseManager.execute(query, models_count, user_id)


class PaymentRepository:
    @staticmethod
    async def save_payment(user_id: str, payment_details: dict) -> None:
        query = """
            INSERT INTO payments (user_id, payment_data)
            VALUES ($1, $2);
        """
        await DatabaseManager.execute(query, user_id, json.dumps(payment_details))
