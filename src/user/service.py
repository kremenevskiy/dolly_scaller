import datetime

from src.model import service as model_service
from src.subscription_details import model as subscription_details_model
from src.subscription_details import service as subscription_details_service
from src.user import exception, model
from src.user.repository import PaymentRepository, UserRepository

user_repository = UserRepository()


async def create_new_user(user: model.User) -> None:
    await user_repository.create_new_user(user)


async def get_user(user_id: str) -> model.User:
    user = await user_repository.get_user_by_id(user_id)
    if user is None:
        raise exception.UserNotFound

    return user


async def get_user_id_from_username(username: str) -> str:
    user_id = await user_repository.get_user_id_from_user_username(username)
    if user_id is None:
        raise exception.UserNotFound
    return user_id


async def add_user_to_whitelist(username: str) -> str:
    user_id = await get_user_id_from_username(username=username)
    await user_repository.add_user_to_whitelist(user_id)
    return user_id


async def delete_user_from_whitelist(username: str) -> None:
    user_id = await get_user_id_from_username(username=username)
    is_success = await user_repository.delete_user_from_whitelist(user_id)
    if not is_success:
        raise exception.UserNotWhitelisted


async def get_active_subcribe(user_id: str) -> model.UserSubscription | None:
    user_sub = await user_repository.get_active_user_subscription(user_id)

    return user_sub


async def subscribe_user(user_id: str, subscription_id: int) -> None:
    subscription = await subscription_details_service.get_subscription_details(
        subscription_id=subscription_id
    )

    new_sub_status = model.SubcriptionStatus.ACTIVE

    active_sub = await user_repository.get_active_user_subscription(user_id)
    if active_sub is not None:
        new_sub_status = model.SubcriptionStatus.PENDING

    if subscription.is_monthly_sub():
        new_user_subscription = model.UserSubscription(
            user_id=user_id,
            subscription_id=subscription_id,
            start_date=datetime.datetime.now(),
            status=new_sub_status,
            end_date=datetime.datetime.now() + datetime.timedelta(days=subscription.duration),
            generation_photos_left=subscription.generation_photos_count,
        )

        await user_repository.save_user_subscription(new_user_subscription)
        await user_repository.increase_user_models_limit(user_id, subscription.models_count)

    elif (
        subscription.subscription_type
        == subscription_details_model.SubscriptionType.GENERATIONS.value
    ):
        if active_sub is None:
            raise exception.NoActiveSubscription

        # Add generations to active subscription
        await user_repository.add_generations_to_active_subscription(
            user_id,
            photos=subscription.generation_photos_left,
        )

    elif subscription.subscription_type == subscription_details_model.SubscriptionType.MODELS.value:
        if active_sub is None:
            raise exception.NoActiveSubscription
        # Increase max models count for user
        await user_repository.increase_user_models_limit(user_id, subscription.models_count)


async def store_user_payment(user_id: str, payment_details: dict) -> None:
    await PaymentRepository.save_payment(user_id, payment_details)


async def update_subscription_state(user_id: str, operation: model.OperationType) -> None:
    user_subscription = await user_repository.get_active_user_subscription(user_id=user_id)
    if user_subscription is None:
        raise exception.NoActiveSubscription

    user = await user_repository.get_user_by_id(user_id=user_id)
    if user is None:
        raise exception.UserNotFound

    if await is_raise_limits(user, user_subscription, operation):
        await handle_raised_limits(user, user_subscription, operation)

    if operation == model.OperationType.GENERATE_BY_IMAGE:
        user_subscription.generation_photos_left -= 1

        await user_repository.update_user_subscription(user_subscription)

    elif operation == model.OperationType.GENERATE_BY_PROMNT:
        user_subscription.generation_photos_left -= 1

        await user_repository.update_user_subscription(user_subscription)


async def check_subscription_limits(user_id: str, operation: model.OperationType) -> None:
    user_subscription = await user_repository.get_active_user_subscription(user_id=user_id)
    if user_subscription is None:
        raise exception.NoActiveSubscription

    user = await user_repository.get_user_by_id(user_id=user_id)
    if user is None:
        raise exception.UserNotFound

    if not user_subscription:
        raise exception.NoActiveSubscription

    if await is_raise_limits(user, user_subscription, operation):
        await handle_raised_limits(user, user_subscription, operation)


async def is_raise_limits(
    user: model.User, user_subscription: model.UserSubscription, operation: model.OperationType
) -> bool:
    if operation == model.OperationType.GENERATE_BY_IMAGE:
        return user_subscription.is_generations_left()

    elif operation == model.OperationType.GENERATE_BY_PROMNT:
        return user_subscription.is_generations_left()

    elif operation == model.OperationType.CREATE_MODEL:
        model_count = await get_user_models_count(user.user_id)
        if model_count >= user.models_max:
            return True

    return False


async def handle_raised_limits(
    user: model.User, user_subcription: model.UserSubscription, operation: model.OperationType
):
    if (
        operation == model.OperationType.GENERATE_BY_IMAGE
        or operation == model.OperationType.GENERATE_BY_PROMNT
    ):
        pending_sub = await UserRepository.get_pending_user_subscription(user.user_id)

        if pending_sub is None:
            raise exception.OperationOutOfLimit(operation)

        raise exception.OperationOutOfLimitWithPending(
            operation,
            user_subcription.generation_photos_left,
            pending_sub.start_date,
        )

    elif operation == model.OperationType.CREATE_MODEL:
        raise exception.OperationOutOfLimit(operation)


async def get_user_models_count(user_id: str) -> int:
    return await model_service.get_user_models_count(user_id)
