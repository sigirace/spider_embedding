from datetime import UTC, datetime
from database.mongo import get_async_mongo_client
from meta.domain.model.meta_shcema import MetaSchema
from meta.domain.repository.meta_repostory import IMetaRepostory


class MetaRepository(IMetaRepostory):
    def __init__(self):
        client = get_async_mongo_client()
        self.db = client[DB]
        self.collection = self.db["meta"]

    async def create_meta(self, meta: MetaSchema) -> MetaSchema:
        meta.created_at = datetime.now(UTC)
        await self.collection.insert_one(meta.model_dump())
        return meta

    async def get_meta(self, app_id: str, meta_id: str) -> MetaSchema:
        raw = await self.collection.find_one(
            {
                "app_id": app_id,
                "id": meta_id,
            },
        )
        if not raw or "metadata" not in raw or not raw["metadata"]:
            return None
        return MetaSchema(**raw["metadata"][0])

    async def get_meta_list(self, app_id: str) -> list[MetaSchema]:

        raw = await self.collection.find_one(
            {
                "app_id": app_id,
            },
            projection={
                "_id": 0,
                "metadata": 1,
            },
        )

        if not raw or "metadata" not in raw or not raw["metadata"]:
            return []

        return [MetaSchema(**item) for item in raw["metadata"]]

    async def delete_meta(self, app_id: str, meta_id: str) -> bool:
        result = await self.collection.update_one(
            {"app_id": app_id},
            {
                "$pull": {"metadata": {"id": meta_id}},
            },
        )
        return result.modified_count > 0

    async def update_meta(self, app_id: str, meta: MetaSchema) -> bool:
        meta.updated_at = datetime.now(UTC)
        result = await self.collection.update_one(
            {"app_id": app_id, "metadata.id": meta.id},
            {"$set": {"metadata.$": meta.model_dump()}},
        )
        return result.modified_count > 0
