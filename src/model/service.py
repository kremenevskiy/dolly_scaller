

from src.model.models import Model
from src.model.repository import ModelRepository


async def generate_model(model: Model):
    await ModelRepository.create_model(model)


async def get_user_models_count(user_id: str) -> int:
    count = await ModelRepository.get_user_model_count(user_id)

    print(user_id)
    print(count)

    return count
