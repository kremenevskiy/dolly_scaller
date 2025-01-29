from typing import List

from fastapi import APIRouter

from src.subscription_details import model, service

subscription_router = APIRouter(prefix="/subscription-details", tags=["Subscriptions"])


@subscription_router.get(
    "/get-active-subscriptions", response_model=List[model.Subscription]
)
async def get_active_subscriptions():
    return await service.get_active_subscriptions()
