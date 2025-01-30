from fastapi import APIRouter

from src.model import service as model_service
from src.schemas import OKResponse
from src.user import model, service

user_router = APIRouter(prefix='/user')


@user_router.post('/create-new-user')
async def create_new_user(user_request: model.User) -> OKResponse:
    await service.create_new_user(user_request)
    return OKResponse(status=True)


@user_router.get('/add-to-whitelist')
async def add_user_to_whitelist(username: str) -> OKResponse:
    await service.add_user_to_whitelist(username=username)
    return OKResponse(status=True)


@user_router.post('/{user_id}/buy-subscription/{subscription_id}')
async def user_buy_subscription(user_id: str, subscription_id: int) -> OKResponse:
    await service.subscribe_user(
        user_id=user_id,
        subscription_id=subscription_id,
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


# class UserCountResponse(OKResponse):
#     models_count: int


# @user_router.get("/{user_id}/models/count", response_model=UserCountResponse)
# async def get_user_model_count(user_id: str):
#     count = await model_service.get_user_models_count(user_id)

#     return UserCountResponse(
#         status=True,
#         models_count=count,
#     )
