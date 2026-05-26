from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import database
from sqlalchemy import text
from routers.project import router as project_router
from routers.place import router as place_router

app = FastAPI(root_path="/api/v1")

app.include_router(project_router)
app.include_router(place_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def entry_path(session: database):
    return await session.execute(text("SELECT 1"))