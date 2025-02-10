from src.subscription_details import exception, model, repository


async def get_active_subscriptions() -> list[model.Subscription]:
    return await repository.SubscriptionRepository.get_active_subscriptions()


async def get_subscription_details(subscription_id: int) -> model.Subscription:
    subscription = await repository.SubscriptionRepository.get_subscription(subscription_id)
    if subscription is None:
        raise exception.SubcriptionNotFound()
    return subscription


async def get_subscription_by_name(sub_name: str) -> model.Subscription:
    sub = await repository.SubscriptionRepository.get_subscription_by_name(sub_name)
    if sub is None:
        raise exception.SubcriptionNotFound()

    return sub 
    
