from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.project import ProjectORM
from database.models.place import PlaceORM
from database.repos.project_repo import ProjectRepo
from database.repos.place_repo import PlaceRepo
from schemas import AddProjectDTO, AddPlaceWithProjectDTO, UpdatePlaceDTO
from fastapi.exceptions import HTTPException
from tools.external_api_call import APIHadnler

class ProjectService:
    def __init__(self, database: AsyncSession) -> None:
        self.database = database
        self.__projectRepo = ProjectRepo(database=database)
        self.__placeRepo = PlaceRepo(database=database)

    async def get_all_projects(self) -> Sequence[ProjectORM]:
        return await self.__projectRepo.select_all_projects()


    async def create_project(self, schema: AddProjectDTO) -> ProjectORM:
        project_database = await self.__projectRepo.add_project(schema=schema)
        if schema.places and len(schema.places) < 11:
            for place in schema.places:
                if not await APIHadnler.check_if_resource_exists(external_id=place.external_id):
                    raise HTTPException(status_code=400, detail="Place ID doesnt exists")
                await self.__placeRepo.add_place(schema=place, project_id=project_database.id)

        await self.database.commit()
        return project_database

    async def select_project_by_id(self, project_id: int) -> ProjectORM:
        project = await self.__projectRepo.select_project_by_id(project_id=project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project Not Found!")
        return project


    async def update_project(self, project_id: int, schema: AddProjectDTO) -> ProjectORM:
        project = await self.select_project_by_id(project_id=project_id)

        result = await self.__projectRepo.update_project(project=project, schema=schema)
        await self.database.commit()
        return result

    async def remove_project(self, project_id: int) -> None:
        project = await self.select_project_by_id(project_id=project_id)
        places = project.places
        for place in places:
            if place.is_visited == True:
                raise HTTPException(status_code=404, detail="Cannot delete project with at list 1 visited place")
        await self.__projectRepo.remove_project(project=project)
        await self.database.commit()
        return

# ================PLACES=====================
    async def create_place(self, project_id, schema: AddPlaceWithProjectDTO):
        project = await self.select_project_by_id(project_id=project_id)
        places_with_same_id_in_project = await self.__placeRepo.select_place_by_external_id_in_project(external_id=schema.external_id, project_id=project_id)
        if places_with_same_id_in_project:
            raise HTTPException(status_code=400, detail="In project already exists place with same external id")
        if len(project.places) == 10:
            raise HTTPException(status_code=404, detail=" cant add more than 10 places")
        if not await APIHadnler.check_if_resource_exists(external_id=schema.external_id):
            raise HTTPException(status_code=400, detail="resource now found!")
        place_database = await self.__placeRepo.add_place(project_id=project_id, schema=schema)
        await self.database.commit()
        await self.database.refresh(place_database)
        return place_database

    async def update_existing_place(self, project_id: int, external_id: str, schema: UpdatePlaceDTO):
        place_database = await self.__placeRepo.select_place_by_external_id_in_project(project_id=project_id, external_id=external_id)

        if not place_database:
            raise HTTPException(status_code=404, detail="Resource doesnt exist!")

        result = await self.__placeRepo.update_place(place=place_database, schema=schema)

        await self.database.flush()

        places_in_project = await self.__placeRepo.select_all_places_by_project_id(project_id=project_id)

        all_visited = all(place.is_visited for place in places_in_project)

        if all_visited:
            result.project.is_completed = True

        await self.database.commit()

        return result

    async def get_all_project_places(self, project_id: int):
        await self.select_project_by_id(project_id=project_id)
        return await self.__placeRepo.select_all_places_by_project_id(project_id=project_id)

    async def get_single_place(self, project_id: int, external_id: str):
        place = await self.__placeRepo.select_place_by_external_id_in_project(project_id=project_id, external_id=external_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found!")
        return place

    async def remove_single_place(self, project_id: int, external_id: str):
        place = await self.get_single_place(project_id=project_id, external_id=external_id)
        await self.__placeRepo.remove_single_place(place=place)
        await self.database.commit()