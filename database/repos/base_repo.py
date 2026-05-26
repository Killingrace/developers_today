from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepo:
    def __init__(self, database: AsyncSession) -> None:
        self.database = database