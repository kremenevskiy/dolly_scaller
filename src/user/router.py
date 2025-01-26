
from fastapi import APIRouter

from src.user import service
from src.user.model import User, UserResponse

user_router = APIRouter(prefix="/user")


@user_router.post("/", response_model=UserResponse)
async def save_user(data: User):
    id = await service.create_user(data)

    return UserResponse(user_id=id)
