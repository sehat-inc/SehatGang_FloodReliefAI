# backend/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import Base, engine
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)
app.include_router(router)
