from datetime import UTC, datetime
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from chunks.domain.model.image_schema import ChunkImageSchema
from chunks.domain.repository.image_repository import IImageRepository
from config import get_settings

DB_CONFIG = get_settings().mongo
DB = DB_CONFIG.mongodb_db


class ImageRepository(IImageRepository):

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client[DB]
        self.collection = self.db["image"]

    async def create_image(
        self,
        image: ChunkImageSchema,
    ) -> ChunkImageSchema:
        image.created_at = datetime.now(UTC)
        await self.collection.insert_one(image.model_dump(by_alias=True))
        return image

    async def get_image(self, image_id: ObjectId) -> ChunkImageSchema | None:

        raw = await self.collection.find_one({"_id": image_id})
        if not raw:
            return None
        return ChunkImageSchema.model_validate(raw)

    async def get_image_by_chunk_id(self, chunk_id: ObjectId) -> List[ChunkImageSchema]:

        raw = await self.collection.find({"chunk_id": chunk_id}).to_list(None)
        return [ChunkImageSchema.model_validate(image) for image in raw]

    async def update_image(self, image_id: ObjectId, image: ChunkImageSchema) -> bool:
        result = await self.collection.update_one(
            {"_id": image_id},
            {"$set": image.model_dump(by_alias=True)},
        )
        return result.modified_count > 0

    async def delete_image(self, image_id: ObjectId) -> bool:

        result = await self.collection.delete_one({"_id": image_id})
        return result.deleted_count > 0
