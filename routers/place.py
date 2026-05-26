from fastapi import APIRouter
from schemas import AddPlaceWithProjectDTO, UpdatePlaceDTO
from services.project_service import ProjectService
from core.database import database

router = APIRouter()


@router.post("/project/{project_id}/place")
async def create_place(project_id: int, schema: AddPlaceWithProjectDTO, database: database):
    return await ProjectService(database=database).create_place(project_id=project_id, schema=schema)


@router.put("/project/{project_id}/place/{external_id}")
async def update_place(project_id: int, schema: UpdatePlaceDTO, database: database, external_id: str):
    return await ProjectService(database=database).update_existing_place(project_id=project_id, external_id=external_id, schema=schema)

@router.get("/project/{project_id}/place")
async def get_all_project_places(project_id: int, database: database):
    return await ProjectService(database=database).get_all_project_places(project_id=project_id)


@router.get("/project/{project_id}/place/{external_id}")
async def get_single_place(project_id: int, external_id: str, database: database):
    return await ProjectService(database=database).get_single_place(external_id=external_id, project_id=project_id)

@router.delete("/project/{project_id}/place/{external_id}", status_code=204)
async def remove_single_place(project_id: int, external_id: str, database: database):
    return await ProjectService(database=database).remove_single_place(external_id=external_id, project_id=project_id)
