import json

from src.database import DatabaseManager
from src.user import model


class UserRepository:
    @staticmethod
    async def create_new_user(user: model.User) -> None:
        query = """
            INSERT INTO users (user_id, username, user_first_name, user_last_name,
                                tg_premium, user_type, models_max, referrer_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (user_id) DO UPDATE
            SET username = EXCLUDED.username,
                user_first_name = EXCLUDED.user_first_name,
                user_last_name = EXCLUDED.user_last_name,
                tg_premium = EXCLUDED.tg_premium,
                user_type = EXCLUDED.user_type,
                models_max = EXCLUDED.models_max,
                referrer_id = EXCLUDED.referrer_id
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
            user.referrer_id,
        )

    @staticmethod
    async def get_user_by_id(user_id: str) -> model.User | None:
        query = """
            SELECT user_id, username, user_first_name, user_last_name, tg_premium,
                user_type, models_max, date_joined, referrer_id
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
    async def delete_user_from_whitelist(user_id: str) -> bool:
        query_check = """
            SELECT user_type FROM users WHERE user_id = $1
        """
        result = await DatabaseManager.fetchrow(query_check, user_id)

        if not result or result['user_type'] == model.UserType.CUSTOMER.value:
            return False

        query_update = """
            UPDATE users
            SET user_type = $1
            WHERE user_id = $2
        """
        await DatabaseManager.execute(query_update, model.UserType.CUSTOMER.value, user_id)
        return True

    @staticmethod
    async def increase_user_models_limit(user_id: str, models_count: int) -> None:
        query = """
            UPDATE users
            SET models_max = COALESCE(models_max, 0) + $1
            WHERE user_id = $2;
        """
        await DatabaseManager.execute(query, models_count, user_id)

    @staticmethod
    async def set_user_models_limit(user_id: str, models_count: int) -> None:
        query = """
            UPDATE users
            SET models_max = $1
            WHERE user_id = $2;
        """
        await DatabaseManager.execute(query, models_count, user_id)

    @staticmethod
    async def count_referral_joins(referrer_id: str) -> int:
        query = """
            SELECT COUNT(*)
            FROM users
            WHERE referrer_id = $1
        """
        return await DatabaseManager.fetchval(query, referrer_id)

    @staticmethod
    async def count_referral_purchases(referrer_id: str) -> int:
        query = """
        SELECT COUNT(*)
        FROM referral_log rl
        WHERE referrer_id = $1;
        """
        return await DatabaseManager.fetchval(query, referrer_id)

    @staticmethod
    async def get_bonus_generations(referrer_id: str) -> int:
        query = """
            SELECT COALESCE(SUM(bonus_generations), 0)
            FROM referral_log
            WHERE referrer_id = $1;
        """
        return await DatabaseManager.fetchval(query, referrer_id)

    @staticmethod
    async def get_user_subscription(
        user_id: str, status: model.SubcriptionStatus
    ) -> model.UserSubscription | None:
        query = """
            SELECT id, subscription_id, user_id, start_date, end_date,
                   generation_photos_left, status
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
                generation_photos_left=row['generation_photos_left'],
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
    async def get_last_user_subscription(
        user_id: str, subscription_id: int
    ) -> model.UserSubscription | None:
        query = """
            SELECT id, subscription_id, user_id, start_date, end_date,
                   generation_photos_left, status
            FROM user_subscriptions
            WHERE user_id = $1 and subscription_id = $2
            ORDER BY start_date desc
            LIMIT 1;
        """
        row = await DatabaseManager.fetchrow(query, user_id, subscription_id)

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
                generation_photos_left=row['generation_photos_left'],
            )
            if row
            else None
        )

    @staticmethod
    async def update_user_subscription(
        user_subscription: model.UserSubscription,
    ) -> None:
        # Update subscription details
        update_subscription_query = """
            UPDATE user_subscriptions
            SET generation_photos_left = generation_photos_left - 1
            WHERE user_id = $1 AND status = 'active';
        """
        await DatabaseManager.execute(
            update_subscription_query,
            user_subscription.user_id,
        )

    @staticmethod
    async def update_user_subscription_status(user_sub: model.UserSubscription) -> None:
        # Update subscription details
        update_subscription_query = """
            UPDATE user_subscriptions
            SET status = $1
            WHERE id = $2;
        """
        await DatabaseManager.execute(
            update_subscription_query,
            user_sub.status.value,
            user_sub.id,
        )

    @staticmethod
    async def save_user_subscription(user_subscription: model.UserSubscription) -> None:
        # Step 2: Insert the new subscription as active
        insert_query = """
            INSERT INTO user_subscriptions (user_id, subscription_id, start_date, end_date, status,
                                            generation_photos_left)
            VALUES ($1, $2, $3, $4, $5, $6);
        """

        await DatabaseManager.execute(
            insert_query,
            user_subscription.user_id,
            user_subscription.subscription_id,
            user_subscription.start_date,
            user_subscription.end_date,
            user_subscription.status.value,
            user_subscription.generation_photos_left,
        )

    @staticmethod
    async def add_generations_to_active_subscription(user_id: str, photos: int) -> None:
        query = """
            UPDATE user_subscriptions
            SET generation_photos_left = generation_photos_left + $1
            WHERE user_id = $2 AND status = 'active';
        """
        await DatabaseManager.execute(query, photos, user_id)

    @staticmethod
    async def add_referral_log(log: model.ReferralLog) -> None:
        query = """
            INSERT INTO referral_log(referrer_id, referral_id, subscription_id, bonus_generations)
                VALUES ($1, $2, $3, $4)
        """

        await DatabaseManager.execute(
            query, log.referrer_id, log.referral_id, log.subscription_id, log.bonus_generations
        )

    @staticmethod
    async def get_ref_bonus_count(user_id: str) -> int:
        query = """
            SELECT COALESCE(SUM(generation_photos_left), 0) as cnt  FROM user_subscriptions
                INNER JOIN subscriptions_details sb on sb.id = subscription_id
                WHERE user_id = $1 and status = 'pending' and
                    sb.subscription_type = 'referral_generations'
        """

        return await DatabaseManager.fetchval(query, user_id)

    @staticmethod
    async def delete_ref_bonus(user_id: str, ref_sub_id: int):
        query = """
            DELETE FROM user_subscriptions WHERE user_id = $1 and
                status = 'pending' and subscription_id = $2
        """

        await DatabaseManager.execute(query, user_id, ref_sub_id)


class PaymentRepository:
    @staticmethod
    async def save_payment(user_id: str, payment_details: dict) -> None:
        query = """
            INSERT INTO payments (user_id, payment_data)
            VALUES ($1, $2);
        """
        await DatabaseManager.execute(query, user_id, json.dumps(payment_details))
