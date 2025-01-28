from fastapi import APIRouter
from pydantic import BaseModel

from src.schemas import OKResponse
from src.user.model import User, UserResponse

from src.user import service
from src.model import service as model_service

user_router = APIRouter(prefix="/user")


@user_router.post("", response_model=UserResponse)
async def save_user(data: User):
    id = await service.create_user(data)

    return UserResponse(user_id=id)


class SubcribeRequest(BaseModel):
    subscribe_id: str


class UserCountResponse(OKResponse):
    models_count: int


@user_router.get("/{user_id}/models/count", response_model=UserCountResponse)
async def get_user_model_count(user_id: str):
    count = await model_service.get_user_models_count(user_id)

    return UserCountResponse(
            status=True,
            models_count=count,
            )


@user_router.post("/{user_id}/subcribe")
async def subcribe_user(user_id: str, req: SubcribeRequest):
    await service.subcribe_user(user_id, req.subscribe_id)

    return OKResponse(
            status=True
            )
