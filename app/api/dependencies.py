from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.repository.users import UserRepository
from app.services.auth_service import AuthService


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(session=db, model=User)
    return AuthService(model=User, user_repo=user_repo)
