from typing import Sequence
from .base_repo import BaseRepo
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from database.models.place import PlaceORM
from database.models.project import ProjectORM
from schemas import AddPlaceWithProjectDTO, UpdatePlaceDTO

class PlaceRepo(BaseRepo):

    async def add_place(self, project_id: int, schema: AddPlaceWithProjectDTO) -> PlaceORM:
        place_database = PlaceORM(
            project_id = project_id,
            external_id = schema.external_id,
            is_visited = schema.is_visited
        )
        self.database.add(place_database)
        return place_database

    async def select_place_by_external_id_in_project(self, external_id: str, project_id: int):
        query = (
            select(PlaceORM)
            .where(PlaceORM.project_id == project_id)
            .where(PlaceORM.external_id == external_id)
            .options(joinedload(PlaceORM.project))
        )
        result = await self.database.execute(query)
        return result.scalars().first()


    async def update_place(self, place: PlaceORM, schema: UpdatePlaceDTO):
        schema_dict = schema.model_dump(exclude_none=True)
        for key, value in schema_dict.items():
            setattr(place, key, value)
        await self.database.flush()
        await self.database.refresh(place)

        return place

    async def select_all_places_by_project_id(self, project_id: int) -> Sequence[PlaceORM]:
        query = (
            select(PlaceORM)
            .where(PlaceORM.project_id == project_id)
        )

        result = await self.database.execute(query)
        return result.scalars().all()

    async def remove_single_place(self, place: PlaceORM) -> None:
        await self.database.delete(place)

        return
