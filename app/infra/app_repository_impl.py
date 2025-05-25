from datetime import UTC, datetime
from typing import List
from bson import ObjectId
from app.domain.model.app_schema import AppSchema
from app.domain.repository.app_repository import IAppRepository
from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient


DB_CONFIG = get_settings().mongo
DB = DB_CONFIG.mongodb_db


class AppRepository(IAppRepository):
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client[DB]
        self.collection = self.db["app"]

    async def create_app(self, app: AppSchema) -> AppSchema:
        app.created_at = datetime.now(UTC)
        await self.collection.insert_one(app.model_dump(by_alias=True))

        return app

    async def get_app(self, oid: ObjectId) -> AppSchema | None:

        raw = await self.collection.find_one(
            {"_id": oid},
        )

        if not raw:
            return None
        return AppSchema.model_validate(raw)

    async def get_app_by_app_name(self, app_name: str) -> AppSchema | None:
        raw = await self.collection.find_one({"app_name": app_name})
        if not raw:
            return None
        return AppSchema.model_validate(raw)

    async def get_app_list(self, user_id: str) -> List[AppSchema]:
        raw = await self.collection.find({"creator": user_id}).to_list(length=None)
        return [AppSchema.model_validate(item) for item in raw]

    async def update_app(self, app: AppSchema) -> bool:

        app.updated_at = datetime.now(UTC)
        result = await self.collection.update_one(
            {"_id": app.id},
            {"$set": app.model_dump(by_alias=True)},
        )
        return result.modified_count > 0

    async def delete_app(self, oid: ObjectId) -> bool:

        result = await self.collection.delete_one(
            {"_id": oid},
        )
        return result.deleted_count > 0
