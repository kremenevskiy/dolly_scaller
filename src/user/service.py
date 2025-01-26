from src.user.model import User
from src.user.repository import UserRepository

user_repository = UserRepository()


async def create_user(user: User) -> str:
    return await user_repository.save_user(user)
