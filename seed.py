from asyncio import run
from core.database import async_engine, BaseORM
from database.models.project import ProjectORM
from database.models.place import PlaceORM

async def create_schema():
    async with async_engine.begin() as connection:
        await connection.run_sync(BaseORM.metadata.drop_all)
        await connection.run_sync(BaseORM.metadata.create_all)





if __name__=="__main__":
    run(create_schema())