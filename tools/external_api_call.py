from core.config import settings
import httpx

class APIHadnler:
    api_link = settings.EXTERNAL_API

    @classmethod
    async def check_if_resource_exists(cls, external_id) -> bool:
        async with httpx.AsyncClient() as conn:
            result = await conn.get(f"{cls.api_link}{external_id}")
            if result.status_code != 200:
                return False
            return True