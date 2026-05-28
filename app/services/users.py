

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repository.users import UserRepository
from app.schema.user import UserCreate
from app.core.security import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create(self, user_create: UserCreate) -> User:
        # convert schema to dict, swap plain password for hashed
        data = user_create.model_dump()
        data["hashed_password"] = get_password_hash(data.pop("password"))

        # delegate insert to BaseRepository.create()
        return await self.repository.create(data)
