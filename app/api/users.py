from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.models.user import User
from app.schema.user import LoginRequest, UserCreate, UserRead
from app.services.auth_service import AuthService

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register", status_code=201, response_model=UserRead)
async def register_user(
    data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return await auth_service.register_user(data)


@user_router.post("/login", response_model=UserRead)
async def login_user(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return await auth_service.login_user(data)
