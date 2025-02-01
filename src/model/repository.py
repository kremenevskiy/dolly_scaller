import json

from src.database import DatabaseManager
from src.model.models import Model


class ModelRepository:
    @staticmethod
    async def get_user_model_count(user_id: str) -> int:
        query = """
            SELECT count(*) as cnt from models where user_id = $1
        """

        row = await DatabaseManager.fetchrow(query, user_id)

        return row['cnt']

    @staticmethod
    async def create_model(model: Model):
        query = """
            INSERT INTO models(name, user_id, gender, link_to_adls, status, photo_info)
            VALUES($1, $2, $3, $4, $5, $6)
        """
        photo_info = json.dumps(model.photo_info)
        await DatabaseManager.execute(
            query,
            model.name,
            model.user_id,
            model.gender.value,
            model.link_to_adls,
            model.status.value,
            photo_info,
        )
