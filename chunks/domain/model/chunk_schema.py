from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from common.model import LifeCycle


class ChunkUpdateSchema(BaseModel):
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(default=[], description="청크 태그")
    images: List[str] = Field(default=[], description="청크 이미지 리스트")


class ChunkDetail(ChunkUpdateSchema):
    page: int = Field(..., description="페이지 번호")
    file_creation_date: Optional[str] = Field(description="파일 생성 일시")
    file_mod_date: Optional[str] = Field(description="파일 수정 일시")


class ChunkSchema(ChunkDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    document_id: ObjectId = Field(..., description="문서 ID, 식별자")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChunkErrorSchema(BaseModel):
    error: str = Field(..., description="청크 생성 실패 이유")


class ChunkDeleteSchema(BaseModel):
    id: str = Field(..., description="청크 ID")
    detail: Optional[str] = Field(default=None, description="청크 삭제 상세 정보")
