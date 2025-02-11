import datetime

from src.logger import logger
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


async def find_user(user_id: str = '', username: str = '') -> model.User:
    if user_id != '':
        return await get_user(user_id)

    if username != '':
        user_id = await get_user_id_from_username(username)

        return await get_user(user_id)

    raise exception.UserNotFound


async def get_user_profile(user: model.User) -> model.UserProfile:
    sub = await get_active_subscribe(user.user_id)

    count = await get_user_models_count(user.user_id)

    referral_info = await get_referral_info(user.user_id)

    return model.UserProfile(
        user=user,
        user_subscription=sub,
        model_count=count,
        referral_info=referral_info,
    )


async def get_user_id_from_username(username: str) -> str:
    user_id = await user_repository.get_user_id_from_user_username(username)
    if user_id is None:
        raise exception.UserNotFound
    return user_id


async def add_user_to_whitelist(username: str) -> str:
    user_id = await get_user_id_from_username(username=username)

    await activate_whitelist_subscription(user_id)
    await user_repository.add_user_to_whitelist(user_id)

    return user_id


async def activate_whitelist_subscription(user_id: str) -> None:
    try:
        await finish_active_sub(user_id)
    except exception.NoActiveSubscription:
        pass

    WHITELIST_GENERATION_COUNT = 1000000
    WHITELIST_MODELS_COUNT = 2

    new_user_subscription = model.UserSubscription(
        user_id=user_id,
        subscription_id=-1,
        start_date=datetime.datetime.now(),
        status=model.SubcriptionStatus.ACTIVE,
        end_date=datetime.datetime.now() + datetime.timedelta(days=365),
        generation_photos_left=WHITELIST_GENERATION_COUNT,
    )

    await user_repository.save_user_subscription(new_user_subscription)
    await user_repository.increase_user_models_limit(user_id, WHITELIST_MODELS_COUNT)


async def finish_active_sub(user_id: str) -> None:
    active_sub = await user_repository.get_active_user_subscription(user_id)
    if active_sub is None:
        raise exception.NoActiveSubscription

    active_sub.status = model.SubcriptionStatus.FINISHED

    await user_repository.update_user_subscription_status(active_sub)


async def delete_user_from_whitelist(username: str) -> None:
    user_id = await get_user_id_from_username(username=username)

    is_success = await user_repository.delete_user_from_whitelist(user_id)
    if not is_success:
        raise exception.UserNotWhitelisted

    await finish_active_sub(user_id)


async def get_active_subscribe(user_id: str) -> model.UserSubscription | None:
    user_sub = await user_repository.get_active_user_subscription(user_id)

    return user_sub


async def get_referral_info(referrer_id: str) -> model.UserReferralInfo:
    referral_joins = await user_repository.count_referral_joins(referrer_id)
    referral_purchases = await user_repository.count_referral_purchases(referrer_id)
    bonus_generations = await user_repository.get_bonus_generations(referrer_id)
    return model.UserReferralInfo(
        referral_joins=referral_joins,
        referral_purchases=referral_purchases,
        bonus_generations=bonus_generations,
    )


async def subscribe_user(
    user_id: str, subscription_id: int
) -> model.UserSubscriptionAdditional | None:
    await apply_subscription(user_id, subscription_id)
    ref_additional = await reward_ref(user_id, subscription_id)
    if ref_additional is not None:
        return model.UserSubscriptionAdditional(
            referral_info=ref_additional,
        )

    return None


async def apply_subscription(user_id: str, subscription_id: int) -> None:
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

        if active_sub is None:
            await add_bonus_ref_count(new_user_subscription)

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
            photos=subscription.generation_photos_count,
        )

    elif subscription.subscription_type == subscription_details_model.SubscriptionType.MODELS.value:
        if active_sub is None:
            raise exception.NoActiveSubscription
        # Increase max models count for user
        await user_repository.increase_user_models_limit(user_id, subscription.models_count)

    elif (
        subscription.subscription_type
        == subscription_details_model.SubscriptionType.REFERRAL_GENERATIONS.value
    ):
        if active_sub is not None:
            return await user_repository.add_generations_to_active_subscription(
                user_id,
                subscription.generation_photos_count,
            )

        new_user_subscription = model.UserSubscription(
            user_id=user_id,
            subscription_id=subscription_id,
            start_date=datetime.datetime.now(),
            status=model.SubcriptionStatus.PENDING,
            end_date=datetime.datetime.now() + datetime.timedelta(days=subscription.duration),
            generation_photos_left=subscription.generation_photos_count,
        )

        await user_repository.save_user_subscription(new_user_subscription)


async def reward_ref(user_id: str, sub_id: int) -> model.ReferralBonusGenerations | None:
    user = await get_user(user_id)

    if user.referrer_id is None:
        return

    ref_sub = await ref_subscription()

    await apply_subscription(user.referrer_id, ref_sub.id)
    await add_referral_log(
        model.ReferralLog(
            referrer_id=user.referrer_id,
            referral_id=user.user_id,
            subscription_id=sub_id,
            bonus_generations=ref_sub.generation_photos_count,
        )
    )

    return model.ReferralBonusGenerations(
        referrer_id=user.referrer_id, bonus_count=ref_sub.generation_photos_count
    )


async def add_bonus_ref_count(active_sub: model.UserSubscription) -> int:
    bonus_count = await user_repository.get_ref_bonus_count(active_sub.user_id)
    print(f'bonus: {bonus_count}')
    active_sub.generation_photos_left += bonus_count
    print(f'active_sub.generation_photos_left: {active_sub.generation_photos_left}')
    ref_sub = await ref_subscription()

    await user_repository.delete_ref_bonus(active_sub.user_id, ref_sub.id)

    return bonus_count


async def ref_subscription() -> subscription_details_model.Subscription:
    return await subscription_details_service.get_subscription_by_name(
        'referral_generations_base_pack'
    )


async def refund_user(user_id: str, subscription_id: int):
    subscription = await subscription_details_service.get_subscription_details(
        subscription_id=subscription_id
    )

    active_sub = await user_repository.get_active_user_subscription(user_id)
    if active_sub is None:
        raise exception.NoActiveSubscription

    if subscription.is_monthly_sub():
        last_sub = await user_repository.get_last_user_subscription(user_id, subscription_id)
        if last_sub is None:
            raise exception.NoActiveSubscription

        last_sub.status = model.SubcriptionStatus.INACTIVE

        await user_repository.update_user_subscription_status(last_sub)
        await user_repository.increase_user_models_limit(user_id, -subscription.models_count)

    elif (
        subscription.subscription_type
        == subscription_details_model.SubscriptionType.GENERATIONS.value
    ):
        if active_sub is None:
            raise exception.NoActiveSubscription

        # Add generations to active subscription
        await user_repository.add_generations_to_active_subscription(
            user_id,
            photos=-subscription.generation_photos_count,
        )

    elif subscription.subscription_type == subscription_details_model.SubscriptionType.MODELS.value:
        if active_sub is None:
            raise exception.NoActiveSubscription
        # Increase max models count for user
        await user_repository.increase_user_models_limit(user_id, -subscription.models_count)


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
    user: model.User, user_subscription: model.UserSubscription, operation: model.OperationType
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
            user_subscription.generation_photos_left,
            pending_sub.start_date,
        )

    elif operation == model.OperationType.CREATE_MODEL:
        raise exception.OperationOutOfLimit(operation)


async def get_user_models_count(user_id: str) -> int:
    return await model_service.get_user_models_count(user_id)


async def update_user_limits(user_id: str, generation_count: int, models_count: int):
    user_subscription = await user_repository.get_active_user_subscription(user_id=user_id)
    if user_subscription is None:
        raise exception.NoActiveSubscription

    await user_repository.increase_user_models_limit(user_id, models_count)
    await user_repository.add_generations_to_active_subscription(
        user_id,
        photos=generation_count,
    )


async def add_referral_log(log: model.ReferalLog):
    await user_repository.add_referral_log(log)
