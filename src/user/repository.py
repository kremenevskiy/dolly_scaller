import json

from src.database import DatabaseManager
from src.user import model


class UserRepository:
    @staticmethod
    async def create_new_user(user: model.User) -> None:
        query = """
            INSERT INTO users (user_id, username, user_first_name, user_last_name,
                                tg_premium, user_type, models_max)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (user_id) DO UPDATE
            SET username = EXCLUDED.username,
                user_first_name = EXCLUDED.user_first_name,
                user_last_name = EXCLUDED.user_last_name,
                tg_premium = EXCLUDED.tg_premium,
                user_type = EXCLUDED.user_type,
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
            user.models_max,
        )

    @staticmethod
    async def get_user_by_id(user_id: str) -> model.User | None:
        query = """
            SELECT user_id, username, user_first_name, user_last_name, tg_premium,
                user_type, models_max, date_joined
            FROM users
            WHERE user_id = $1;
        """
        row = await DatabaseManager.fetchrow(query, user_id)

        return model.User.from_row(row) if row else None

    @staticmethod
    async def get_user_id_from_user_username(username: str) -> str | None:
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
        # Step 2: Insert the new subscription as active
        insert_query = """
            INSERT INTO user_subscriptions (user_id, subscription_id, start_date, end_date, status,
                                            photos_by_prompt_left, photos_by_image_left)
            VALUES ($1, $2, $3, $4, $5, $6, $7);
        """

        await DatabaseManager.execute(
            insert_query,
            user_subscription.user_id,
            user_subscription.subscription_id,
            user_subscription.start_date,
            user_subscription.end_date,
            user_subscription.status.value,
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
            WHERE user_id = $3 AND status = 'active';
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

    @staticmethod
    @staticmethod
    async def get_user_subscription(
        user_id: str, status: model.SubcriptionStatus
    ) -> model.UserSubscription | None:
        query = """
            SELECT id, subscription_id, user_id, start_date, end_date,
                   photos_by_prompt_left, photos_by_image_left, status
            FROM user_subscriptions
            WHERE user_id = $1 AND status = $2
            LIMIT 1;
        """
        row = await DatabaseManager.fetchrow(query, user_id, status.value)

        if not row:
            return None

        return (
            model.UserSubscription(
                id=row['id'],
                subscription_id=row['subscription_id'],
                user_id=row['user_id'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                status=row['status'],
                photos_by_prompt_left=row['photos_by_prompt_left'],
                photos_by_image_left=row['photos_by_image_left'],
            )
            if row
            else None
        )

    @staticmethod
    async def get_pending_user_subscription(user_id: str) -> model.UserSubscription | None:
        return await UserRepository.get_user_subscription(user_id, model.SubcriptionStatus.PENDING)

    @staticmethod
    async def get_active_user_subscription(user_id: str) -> model.UserSubscription | None:
        return await UserRepository.get_user_subscription(user_id, model.SubcriptionStatus.ACTIVE)

    @staticmethod
    async def update_user_subscription(
        user_subscription: model.UserSubscription,
    ) -> None:
        # Update subscription details
        update_subscription_query = """
            UPDATE user_subscriptions
            SET photos_by_prompt_left = $1,
                photos_by_image_left = $2
            WHERE user_id = $3 AND status = 'active';
        """
        await DatabaseManager.execute(
            update_subscription_query,
            user_subscription.photos_by_prompt_left,
            user_subscription.photos_by_image_left,
            user_subscription.user_id,
        )


class PaymentRepository:
    @staticmethod
    async def save_payment(user_id: str, payment_details: dict) -> None:
        query = """
            INSERT INTO payments (user_id, payment_data)
            VALUES ($1, $2);
        """
        await DatabaseManager.execute(query, user_id, json.dumps(payment_details))
