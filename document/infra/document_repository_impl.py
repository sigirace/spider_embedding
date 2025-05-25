from datetime import UTC, datetime
from typing import List, Optional

from bson import ObjectId

from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

from document.domain.model.document_schema import DocumentSchema
from document.domain.repository.document_repository import IDocumentRepository

DB_CONFIG = get_settings().mongo
DB = DB_CONFIG.mongodb_db


class DocumentRepository(IDocumentRepository):
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client[DB]
        self.collection = self.db["document"]

    async def create_document(self, document: DocumentSchema) -> DocumentSchema:
        document.created_at = datetime.now(UTC)
        await self.collection.insert_one(document.model_dump(by_alias=True))

        return document

    async def exist_document(self, app_id: str, hash: str, size: int) -> bool:
        return (
            await self.collection.find_one(
                {"app_id": app_id, "hash": hash, "size": size},
                projection={"_id": 1},
            )
            is not None
        )

    async def get_document(self, document_id: ObjectId) -> Optional[DocumentSchema]:
        raw = await self.collection.find_one({"_id": document_id})

        if not raw:
            return None

        return DocumentSchema.model_validate(raw)

    async def get_document_list(self, app_id: ObjectId) -> List[DocumentSchema]:
        raw = await self.collection.find({"app_id": app_id}).to_list(length=None)

        if not raw:
            return []

        return [DocumentSchema.model_validate(doc) for doc in raw]

    async def update_document(self, document: DocumentSchema) -> bool:
        document.updated_at = datetime.now(UTC)
        result = await self.collection.update_one(
            {"_id": ObjectId(document.id)},
            {"$set": document.model_dump(by_alias=True)},
        )
        return result.modified_count > 0

    async def delete_document(self, document_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": document_id})
        return result.deleted_count > 0
