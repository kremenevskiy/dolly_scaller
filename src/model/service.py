

from src.model.models import Model
from src.model.repository import ModelRepository


repo = ModelRepository()


async def generate_model(model: Model):
    await repo.create_model(model)


async def get_user_models_count(user_id: str) -> int:
    count = await repo.get_user_model_count(user_id)

    return count
