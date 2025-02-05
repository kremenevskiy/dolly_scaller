from src.database import DatabaseManager
from src.subscription_details import model


class SubscriptionRepository:
    @staticmethod
    async def get_active_subscriptions() -> list[model.Subscription]:
        query = """
            SELECT id, subscription_name, subscription_type, cost_rubles, cost_stars,
                duration, start_date, end_date,
                models_count, generation_photos_count
            FROM subscriptions_details
            WHERE is_active = TRUE;
        """
        rows = await DatabaseManager.fetch(query)
        return [model.Subscription.from_row(row) for row in rows]

    @staticmethod
    async def get_subscription(subscription_id: int) -> model.Subscription | None:
        query = """
            SELECT id, subscription_name, subscription_type, cost_rubles, cost_stars,
                duration, start_date, end_date,
                models_count, generation_photos_count
            FROM subscriptions_details
            WHERE id = $1;
        """
        row = await DatabaseManager.fetchrow(query, subscription_id)
        return model.Subscription.from_row(row) if row else None
