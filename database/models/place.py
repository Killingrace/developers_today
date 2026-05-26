from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from core.database import BaseORM

class PlaceORM(BaseORM):
    __tablename__="place"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"))
    external_id: Mapped[str]
    notes: Mapped[str] = mapped_column(String(256), nullable=True, default=None)
    is_visited: Mapped[bool] = mapped_column(default=False)

    project: Mapped["ProjectORM"] = relationship(  # type: ignore
        "ProjectORM",
        back_populates="places",
    )