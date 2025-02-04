from fastapi import APIRouter

from src.schemas import OKResponse
from src.user_profile import model, service

user_profile_router = APIRouter(prefix='/user-profile', tags=['User Profile'])


@user_profile_router.get('/photo-formats', response_model=list[model.PhotoFormat])
async def get_photo_formats():
    return await service.get_photo_formats()


@user_profile_router.get('/{user_id}/user-photo-format', response_model=model.PhotoFormat)
async def get_user_photo_format(user_id: str):
    return await service.get_user_photo_format(user_id=user_id)


@user_profile_router.post('/change-photo-format')
async def change_user_photo_format(format_request: model.UserProfile) -> OKResponse:
    await service.change_user_photo_format(
        user_id=format_request.user_id, format_id=format_request.format_id
    )

    return OKResponse(status=True)
