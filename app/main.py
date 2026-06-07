from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.db import get_db
from app.api.users import user_router
import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy

app = FastAPI()

app.include_router(user_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World", "message": "I am creating a FastAPI application!"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}