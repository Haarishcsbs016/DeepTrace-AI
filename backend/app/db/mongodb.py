from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

_client: AsyncIOMotorClient | None = None
_db = None


async def connect_mongo():
    global _client, _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.MONGODB_URL)
    _db = _client[settings.MONGODB_DB]


async def close_mongo():
    global _client
    if _client:
        _client.close()
        _client = None


def get_db():
    return _db
