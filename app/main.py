from fastapi import FastAPI
from app.api import users, records
from app.models import user, record
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///./finance.db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI(title="Finance Backend")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(records.router, prefix="/api/records", tags=["records"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(record.Base.metadata.create_all)