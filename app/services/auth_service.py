

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.users import UserRepository
from app.schema.user import LoginRequest, UserCreate
from app.utils.security import get_password_hash, verify_password
from app.core.repositories.base import BaseRepository
from app.core.exceptions.exceptions import BadRequestException


class AuthService(BaseRepository[User]):
    """
    Authentication service that provides user registration and authentication
    related operations. Extends the BaseRepository to leverage common database
    operations for the User model.
    """

    def __init__(self, model: type[User], user_repo: UserRepository) -> None:
        self.user_repo = user_repo
            

    async def register_user(self, data: UserCreate) -> User:
        user = await self.user_repo.get_by_email(data.email)
        if user:
            raise BadRequestException("User already exists with this email")

        Password = get_password_hash(data.password, salt=None)
        
        return await self.user_repo.create(
            {
                "email": data.email,
                "username": data.username,
                "hashed_password": Password,
            }
        )

    async def login_user(self, data: LoginRequest) -> User:
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise BadRequestException("Invalid credentials")
        is_valid, _ = verify_password(data.password, user.hashed_password)
        if not is_valid:
            raise BadRequestException("Invalid credentials")
        return user

