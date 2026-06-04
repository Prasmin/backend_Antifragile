

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.users import UserRepository
from app.schema.user import UserCreate
from app.utils.security import get_password_hash, verify_password
from app.core.repositories.base import BaseRepository


class AuthService(BaseRepository[User]):
    """
    Authentication service that provides user registration and authentication
    related operations. Extends the BaseRepository to leverage common database
    operations for the User model.
    """

    def __init__(self, model: type[User], user_repo: UserRepository) -> None:
        self.user_repo = user_repo
            

    async def verify_user(self, username: str, password: str) -> User | None:
        user = await self.user_repo.get_by_username(username)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
