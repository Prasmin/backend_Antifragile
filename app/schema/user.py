from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str          # raw — you hash it before saving
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    uuid: UUID
    email: EmailStr
    username: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # allows ORM → Pydantic

class UserUpdate(BaseModel):
    username: str 
    password: str
