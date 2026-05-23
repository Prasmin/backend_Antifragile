from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str          # raw — you hash it before saving
    username: str

class UserRead(UserCreate):
    id: int
    uuid: UUID
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # allows ORM → Pydantic

class UserUpdate(UserCreate):
    username: str 
    password: str 