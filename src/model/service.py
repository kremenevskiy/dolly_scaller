from src.model.models import Model
from src.model.repository import ModelRepository


async def generate_model(model: Model) -> None:
    await ModelRepository.create_model(model)


async def get_user_models_count(user_id: str) -> int:
    return await ModelRepository.get_user_model_count(user_id)
