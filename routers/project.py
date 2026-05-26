from fastapi import APIRouter
from core.database import database
from services.project_service import ProjectService
from schemas import AddProjectDTO
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.get("/project")
async def get_project(database: database):
    return await ProjectService(database=database).get_all_projects()


@router.post("/project")
async def create_project(database: database, schema: AddProjectDTO):
    return await ProjectService(database=database).create_project(schema=schema)

@router.get("/project/{project_id}")
async def get_single_project(database: database, project_id: int):
    return await ProjectService(database=database).select_project_by_id(project_id=project_id)

@router.put("/project/{project_id}")
async def update_project(project_id: int, schema: AddProjectDTO, database: database):
    return await ProjectService(database=database).update_project(project_id=project_id, schema=schema)


@router.delete("/project/{project_id}", status_code=204)
async def delete_project(project_id: int, database: database):
    return await ProjectService(database=database).remove_project(project_id=project_id)

