from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.repository.users import UserRepository
from app.services.auth_service import AuthService
from app.services.journal_service import JournalService


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(session=db, model=User)
    return AuthService(model=User, user_repo=user_repo)


def get_journal_service() -> JournalService:
    return JournalService()
