from fastapi import APIRouter
from pydantic import BaseModel

from src.exceptions import NotFound
from src.schemas import OKResponse
from src.user import (
    model,
    service,
)
from src.user.exception import NoActiveSubscription


user_router = APIRouter(prefix='/user')


@user_router.post('/create-new-user')
async def create_new_user(user_request: model.User) -> OKResponse:
    await service.create_new_user(user_request)

    return OKResponse(status=True)


class UserProfile(BaseModel):
    user: model.User
    user_subscription: model.UserSubscription
    model_count: int


@user_router.get('/{user_id}')
async def user_profile(user_id: str) -> UserProfile:
    user = await service.get_user(user_id)

    sub = await service.get_active_subcribe(user_id)
    if sub is None:
        raise NoActiveSubscription()

    count = await service.get_user_models_count(user_id)

    return UserProfile(user=user, user_subscription=sub, model_count=count)


@user_router.get('/add-to-whitelist')
async def add_user_to_whitelist(username: str) -> OKResponse:
    await service.add_user_to_whitelist(username=username)
    return OKResponse(status=True)


class SubcribeRequest(BaseModel):
    subcription_id: int


@user_router.post('/{user_id}/subcribe')
async def user_buy_subscription(user_id: str, req: SubcribeRequest) -> OKResponse:
    await service.subscribe_user(
        user_id=user_id,
        subscription_id=req.subcription_id,
    )

    return OKResponse(status=True)


@user_router.post('/{user_id}/add-payment-info')
async def user_add_payment_info(
    user_id: str,
    payment_details: model.PaymentDetails,
) -> OKResponse:
    await service.store_user_payment(
        user_id=user_id,
        payment_details=payment_details.model_dump(),
    )
    return OKResponse(status=True)


@user_router.get('/{user_id}/subcription')
async def active_subscription(user_id: str) -> OKResponse:
    sub = await service.get_active_subcribe(user_id)
    if sub is None:
        raise NotFound()

    return OKResponse(status=True)


@user_router.get('/{user_id}/limit/model')
async def check_user_model_limit(user_id: str) -> OKResponse:
    await service.check_subscription_limits(user_id, model.OperationType.CREATE_MODEL)

    return OKResponse(status=True)
