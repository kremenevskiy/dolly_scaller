from src.user_profile import exception, model, repository


async def get_photo_formats() -> list[model.PhotoFormat]:
    formats = await repository.UserProfileRepository.get_photo_formats()
    if not formats:
        raise exception.FormatsNotFound

    return formats


async def get_user_photo_format(user_id: str) -> model.PhotoFormat:
    photo_format = await repository.UserProfileRepository.get_user_photo_format(user_id=user_id)
    print(f'photo format when exists: {photo_format}')
    if not photo_format:
        formats = await repository.UserProfileRepository.get_photo_formats()
        await repository.UserProfileRepository.change_user_photo_format(
            user_id=user_id, format_id=formats[0].id
        )
        photo_format = await repository.UserProfileRepository.get_user_photo_format(user_id=user_id)
    return photo_format


async def change_user_photo_format(user_id: str, format_id: int) -> None:
    await repository.UserProfileRepository.change_user_photo_format(
        user_id=user_id, format_id=format_id
    )
