

from src.subcription.models import Subcription
from src.subcription.repository import SubcriptionRepository

repo = SubcriptionRepository()


async def get_subcription(subcription_id: str) -> Subcription:
    return await repo.get_subcription(subcription_id)
