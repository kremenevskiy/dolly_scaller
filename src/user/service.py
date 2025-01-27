from enum import Enum
from src.user.exception import OperationOutOfLimit
from src.user.model import User
from src.user.repository import UserRepository
from src.subcription import service as subcription_service

user_repository = UserRepository()


class OperationType(Enum):
    GENERATE_BY_IMAGE = "generate_by_image"
    GENERATE_BY_PROMNT = "generate_by_prompt"
    CREATE_MODEL = "create_model"


async def create_user(user: User) -> str:
    return await user_repository.save_user(user)


async def check_limits(user_id: str, operation: OperationType) -> str:
    user = await user_repository.get_user(user_id)

    user_sub_state = await user_repository.get_user_subcription_state(user)

    if operation == OperationType.GENERATE_BY_IMAGE:
        user_sub_state.photo_by_image_count -= 1
        if user_sub_state.photo_by_image_count <= 0:
            raise OperationOutOfLimit(operation)

    elif operation == OperationType.GENERATE_BY_PROMNT:
        user_sub_state.photo_by_promnt_count -= 1
        if user_sub_state.photo_by_promnt_count <= 0:
            raise OperationOutOfLimit(operation)

    elif operation == OperationType.CREATE_MODEL:

    return ''
