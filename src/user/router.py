from fastapi import APIRouter
from pydantic import BaseModel

from src.model import service as model_service
from src.schemas import OKResponse
from src.user import service
from src.user.model import User, UserResponse

user_router = APIRouter(prefix="/user")


@user_router.post("/create-new-user", response_model=OKResponse)
async def create_new_user(user_request: User):
    await service.create_new_user(user_request)
    return OKResponse(status=True)


@user_router.get("/get-id-from-username", response_model=dict)
async def get_user_id_from_username(username: str):
    user_id = await service.get_user_id_from_username(username)
    return {"user_id": user_id}


# class SubcribeRequest(BaseModel):
#     subscribe_id: str


# class UserCountResponse(OKResponse):
#     models_count: int


# @user_router.get("/{user_id}/models/count", response_model=UserCountResponse)
# async def get_user_model_count(user_id: str):
#     count = await model_service.get_user_models_count(user_id)

#     return UserCountResponse(
#         status=True,
#         models_count=count,
#     )


# @user_router.post("/{user_id}/subcribe")
# async def subcribe_user(user_id: str, req: SubcribeRequest):
#     await service.subcribe_user(user_id, req.subscribe_id)

#     return OKResponse(status=True)
