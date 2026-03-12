from fastapi import FastAPI

from app.database import engine, Base
from app import cpes

app = FastAPI(
    title="NVD CPE API",
    version="1.0.0",
)
app.include_router(cpes.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)