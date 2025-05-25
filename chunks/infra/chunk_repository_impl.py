from datetime import UTC, datetime
from motor.motor_asyncio import AsyncIOMotorClient
from chunks.domain.model.chunk_schema import ChunkSchema
from chunks.domain.repository.chunk_repository import IChunkRepository
from config import get_settings

DB_CONFIG = get_settings().mongo
DB = DB_CONFIG.mongodb_db


class ChunkRepository(IChunkRepository):

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client[DB]
        self.collection = self.db["chunk"]

    async def create_chunk(self, chunk: ChunkSchema) -> ChunkSchema:
        chunk.created_at = datetime.now(UTC)
        await self.collection.insert_one(chunk.model_dump(by_alias=True))

        return chunk
