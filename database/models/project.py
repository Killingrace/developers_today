from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.database import BaseORM
from .place import PlaceORM

class ProjectORM(BaseORM):
    __tablename__="project"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    start_date: Mapped[date] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)

    places: Mapped[list[PlaceORM]] = relationship(
        PlaceORM,
        foreign_keys=[PlaceORM.project_id],
        cascade="all, delete-orphan"
    )