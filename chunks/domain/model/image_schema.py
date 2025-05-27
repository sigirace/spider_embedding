from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from common.model import LifeCycle


class ChunkImageSchema(LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    chunk_id: ObjectId = Field(..., description="청크 ID")
    image_url: str = Field(..., description="이미지 URL")
    image_description: Optional[str] = Field(None, description="이미지 설명")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
