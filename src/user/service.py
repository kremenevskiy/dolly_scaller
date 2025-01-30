import datetime

from src.model import service as model_service
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


async def update_sub_state(user: model.User, operation: model.OperationType) -> None:
    user_sub_state = await user_repository.get_user_subcription_state(user.user_id)

    if operation == OperationType.GENERATE_BY_IMAGE:
        user_sub_state.photo_by_image_count -= 1
        if user_sub_state.photo_by_image_count <= 0:
            raise OperationOutOfLimit(operation)

    elif operation == OperationType.GENERATE_BY_PROMNT:
        user_sub_state.photo_by_promnt_count -= 1
        if user_sub_state.photo_by_promnt_count <= 0:
            raise OperationOutOfLimit(operation)

    elif operation == OperationType.CREATE_MODEL:
        count = await model_service.get_user_models_count(user.user_id)

        if count >= user.models_max:
            raise OperationOutOfLimit(operation)

    await user_repository.save_user_sub_state(user_sub_state)
