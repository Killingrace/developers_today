from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AddProjectDTO(BaseDTO):
    name: str = Field(max_length=64)
    desription: str | None = Field(default=None, max_length=256)
    start_date: date | None = None
    is_completed: bool = False
    places: list[AddPlaceWithProjectDTO] | None


class UpdatePlaceDTO(BaseDTO):
    notes: str | None = Field(default=None, max_length=256)
    is_visited: bool = False

class AddPlaceWithProjectDTO(UpdatePlaceDTO):
    external_id: str

class AddPlaceDTO(AddPlaceWithProjectDTO):
    project_id: int