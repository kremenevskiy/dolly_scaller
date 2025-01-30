import datetime

from src.subscription_details import model as subscription_details_model
from src.subscription_details import service as subscription_details_service
from src.user import exception, model
from src.user.repository import PaymentRepository, UserRepository

user_repository = UserRepository()


async def create_new_user(user: model.User) -> None:
    await user_repository.create_new_user(user)


async def get_user_id_from_username(username: str) -> str:
    user_id = await user_repository.get_user_id_from_user_username(username)
    if user_id is None:
        raise exception.UserNotFound()
    return user_id


async def add_user_to_whitelist(username: str) -> None:
    user_id = await get_user_id_from_username(username=username)
    await user_repository.add_user_to_whitelist(user_id)


async def subscribe_user(user_id: str, subscription_id: int) -> None:
    subscription = await subscription_details_service.get_subscription_details(
        subscription_id=subscription_id
    )

    # TODO: Проверить что если уже есть положить в delayed

    if subscription.subscription_type == subscription_details_model.SubscriptionType.MONTHLY.value:
        new_user_subscription = model.UserSubscription(
            user_id=user_id,
            subscription_id=subscription_id,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=subscription.duration),
            photos_by_prompt_left=subscription.photos_by_prompt_count,
            photos_by_image_left=subscription.photos_by_image_count,
        )
        await user_repository.save_user_subscription(new_user_subscription)

    elif (
        subscription.subscription_type
        == subscription_details_model.SubscriptionType.GENERATIONS.value
    ):
        # Add generations to active subscription
        await user_repository.add_generations_to_active_subscription(
            user_id,
            photos_by_prompt=subscription.photos_by_prompt_count,
            photos_by_image=subscription.photos_by_image_count,
        )

    elif subscription.subscription_type == subscription_details_model.SubscriptionType.MODELS.value:
        # Increase max models count for user
        await user_repository.increase_user_models_limit(user_id, subscription.models_count)


async def store_user_payment(user_id: str, payment_details: dict) -> None:
    await PaymentRepository.save_payment(user_id, payment_details)


async def update_subscription_state(user_id: str, operation: model.OperationType) -> None:
    user_subscription = await user_repository.get_active_user_subscription(user_id=user_id)
    user = await user_repository.get_user_by_id(user_id=user_id)

    if not user_subscription:
        raise exception.NoActiveSubscription('User has no active subscription')

    if operation == model.OperationType.CREATE_MODEL:
        user.models_created += 1

    elif operation == model.OperationType.GENERATE_BY_IMAGE:
        user_subscription.photos_by_image_left -= 1

    elif operation == model.OperationType.GENERATE_BY_PROMNT:
        user_subscription.photos_by_prompt_left -= 1

    update_models = operation == model.OperationType.CREATE_MODEL
    await user_repository.update_user_subscription(
        user_subscription=user_subscription, user=user, update_models=update_models
    )


async def check_subscription_limits(user_id: str, operation: model.OperationType) -> None:
    user_subscription = await user_repository.get_active_user_subscription(user_id=user_id)
    user = await user_repository.get_user_by_id(user_id=user_id)

    if not user_subscription:
        raise exception.NoActiveSubscription()

    if operation == model.OperationType.GENERATE_BY_IMAGE:
        if user_subscription.photos_by_image_left <= 0:
            raise exception.OperationOutOfLimit(operation)

    elif operation == model.OperationType.GENERATE_BY_PROMNT:
        if user_subscription.photos_by_prompt_left <= 0:
            raise exception.OperationOutOfLimit(operation)

    elif operation == model.OperationType.CREATE_MODEL:
        if user.models_created >= user.models_max:
            raise exception.OperationOutOfLimit(operation)
