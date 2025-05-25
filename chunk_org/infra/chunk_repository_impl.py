from fastapi import HTTPException
from database.mongo import get_async_mongo_client
from chunk_org.domain.model.chunk_schema import ChunkSchema
from chunk_org.domain.repository.chunk_repository import IChunkRepository
from config import get_settings

DB_CONFIG = get_settings().mongo
DB = DB_CONFIG.mongodb_db


class ChunkRepository(IChunkRepository):

    def __init__(self):
        client = get_async_mongo_client()
        self.db = client[DB]
        self.collection = self.db["app"]

    async def create_chunk_bulk(
        self,
        app_id: str,
        meta_id: str,
        chunk_list: list[ChunkSchema],
    ) -> None:

        # MongoDB에 저장할 데이터 구조 (dict 형태로 변환)
        chunk_dicts = [chunk.model_dump() for chunk in chunk_list]

        # 업데이트 쿼리
        result = await self.collection.update_one(
            {"app_id": app_id, "metadata.id": meta_id},
            {"$push": {"metadata.$.chunks": {"$each": chunk_dicts}}},
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail=f"변경된 데이터가 없습니다. app_id: {app_id}, meta_id: {meta_id}",
            )

    async def delete_chunk_bulk(
        self,
        app_id: str,
        meta_id: str,
    ) -> bool:
        """
        특정 app_id 및 meta_id에 해당하는 metadata의 chunks를 전부 삭제합니다.
        """
        result = await self.collection.update_one(
            {"app_id": app_id, "metadata.id": meta_id},
            {"$set": {"metadata.$.chunks": []}},
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail="App 또는 Meta를 찾을 수 없습니다."
            )

        # 실제 chunks가 비워졌는지 확인
        return result.modified_count > 0

    def update_chunk(
        self,
        app_id: str,
        meta_id: str,
        chunk: ChunkSchema,
    ) -> bool:
        pass
