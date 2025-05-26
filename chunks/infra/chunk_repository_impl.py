from datetime import UTC, datetime
from typing import List
from bson import ObjectId
from fastapi import HTTPException
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

    async def create_chunk(
        self,
        chunk: ChunkSchema,
    ) -> ChunkSchema:
        await self.collection.insert_one(chunk.model_dump(by_alias=True))
        return chunk

    async def get_chunk(self, chunk_id: ObjectId) -> ChunkSchema | None:

        raw = await self.collection.find_one({"_id": chunk_id})
        if not raw:
            return None
        return ChunkSchema.model_validate(raw)

    async def get_chunk_by_document_id(
        self, document_id: ObjectId
    ) -> List[ChunkSchema]:

        raw = await self.collection.find({"document_id": document_id}).to_list(None)
        return [ChunkSchema.model_validate(chunk) for chunk in raw]

    async def delete_chunk(self, chunk_id: ObjectId) -> bool:

        result = await self.collection.delete_one({"_id": chunk_id})
        return result.deleted_count > 0
