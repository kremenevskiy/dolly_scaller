from src.subscription_details import model, repository


async def get_active_subscriptions() -> list[model.Subscription]:
    return await repository.SubscriptionRepository.get_active_subscriptions()
