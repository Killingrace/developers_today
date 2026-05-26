from .base_repo import BaseRepo
from sqlalchemy import select
from database.models.project import ProjectORM
from schemas import AddProjectDTO
from sqlalchemy.orm import selectinload

class ProjectRepo(BaseRepo):
    async def select_all_projects(self):
        query = (
            select(ProjectORM)
        )
        result = await self.database.execute(query)
        return result.scalars().all()

    async def add_project(self, schema: AddProjectDTO) -> ProjectORM:
        database_project = ProjectORM(
            name=schema.name,
            description=schema.desription,
            start_date=schema.start_date,
            is_completed=schema.is_completed
        )
        self.database.add(database_project)
        await self.database.flush()
        await self.database.refresh(database_project)
        return database_project

    async def select_project_by_id(self, project_id: int) -> ProjectORM | None:
        query = (
            select(ProjectORM)
            .where(ProjectORM.id == project_id)
            .options(
                selectinload(ProjectORM.places)
            )
        )
        result = await self.database.execute(query)
        return result.scalar_one_or_none()

    async def update_project(self, project: ProjectORM, schema: AddProjectDTO) -> ProjectORM:
        schema_dict = schema.model_dump(exclude_none=True)
        for key, value in schema_dict.items():
            setattr(project, key, value)
        await self.database.flush()
        await self.database.refresh(project)
        return project

    async def remove_project(self, project: ProjectORM) -> None:
        await self.database.delete(project)
        return

